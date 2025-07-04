import inspect
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional, Tuple, Union

import parse

from pyechonext.mvc.controllers import PageController
from pyechonext.request import Request
from pyechonext.urls import URL
from pyechonext.utils import prepare_url
from pyechonext.utils.exceptions import RoutePathExistsError, URLNotFound
from pyechonext.utils.trie import PrefixTree


class RoutesTypes(Enum):
    """
    This class describes routes types.
    """

    URL_BASED = 0
    PAGE = 1


@dataclass(frozen=True)
class Route:
    """
    This class describes a route.
    """

    page_path: str
    handler: Callable | PageController
    route_type: RoutesTypes
    methods: list = field(default_factory=list)
    summary: Optional[str] = None
    is_dynamic: bool = False  # New flag to indicate dynamic route


def _create_url_route(url: URL) -> Route:
    """Create URL Route

    Args:
        url (URL): URL instance

    Returns:
        Route: route instance
    """
    is_dynamic = "{" in url.path and "}" in url.path
    return Route(
        page_path=url.path,
        handler=url.controller(),
        route_type=RoutesTypes.URL_BASED,
        summary=url.summary,
        is_dynamic=is_dynamic,
    )


def _create_page_route(
    page_path: str,
    handler: Callable,
    methods: Optional[List[str]] = None,
    summary: Optional[str] = None,
) -> Route:
    """Create page route

    Args:
        page_path (str): path of page
        handler (Callable): handler object
        methods (Optional[List[str]]): supported methods. Defaults to None.
        summary (Optional[str], optional): summary docstring. Defaults to None.

    Returns:
        Route: route
    """
    if methods is None:
        methods = ["GET"]

    is_dynamic = "{" in page_path and "}" in page_path
    return Route(
        page_path=page_path,
        handler=handler,
        route_type=RoutesTypes.PAGE,
        methods=methods,
        summary=summary,
        is_dynamic=is_dynamic,
    )


def generate_page_route(
    page_path: str,
    handler: Callable,
    methods: Optional[List[str]] = None,
    summary: Optional[str] = None,
) -> Route:
    """Generate page route

    Args:
        page_path (str): page path url
        handler (Callable): handler object
        methods (Optional[List[str]]): supported methods. Defaults to None.
        summary (Optional[str], optional): summary docstring. Defaults to None.

    Returns:
        Route: created route
    """
    return _create_page_route(page_path, handler, methods, summary)


class Router:
    """
    This class describes a router.
    """

    __slots__ = ("prefix", "urls", "routes", "_trie", "dynamic_routes")

    def __init__(self, urls: Optional[List[URL]] = None, prefix: Optional[str] = None):
        """Initialize a router with urls and routes

        Args:
            urls (Optional[List[URL]], optional): urls list. Defaults to [].
        """
        if urls is None:
            urls = []

        self.prefix = prefix
        self.urls = urls
        self.routes = {}
        self._trie = PrefixTree()
        self.dynamic_routes = []  # Separate storage for dynamic routes
        self._prepare_urls()

    def route_page(
        self,
        page_path: str,
        methods: Optional[List[str]] = None,
        summary: Optional[str] = None,
    ) -> Callable:
        """Route a page

        Args:
            page_path (str): page path
            methods (list, optional): methods list. Defaults to ["GET"].
            summary (Optional[str], optional): summary docstring. Defaults to None.

        Returns:
                Callable: route page wrapper
        """

        if methods is None:
            methods = ["GET"]

        def wrapper(handler: PageController | Callable):
            nonlocal page_path

            page_path = (
                page_path if self.prefix is None else f"{self.prefix}{page_path}"
            )

            if inspect.isclass(handler):
                self.add_url(
                    URL(path=page_path, controller=handler, summary=summary))
            else:
                self.add_page_route(page_path, handler, methods, summary)

            return handler

        return wrapper

    def _prepare_urls(self):
        """
        Prepare URLs (add to routes)
        """
        for url in self.urls:
            path = url.path if self.prefix is None else f"{self.prefix}{url.path}"
            route = _create_url_route(url)

            if route.is_dynamic:
                self.dynamic_routes.append(route)
            else:
                self._trie.insert(path)

            self.routes[path] = route

    def add_page_route(
        self,
        page_path: str,
        handler: Callable,
        methods: Optional[List[str]] = None,
        summary: Optional[str] = None,
    ):
        """Add page route

        Args:
            page_path (str): page path URL
            handler (Callable): handler object
            methods (Optional[List[str]]): supported methods of handler. Defaults to None.
            summary (Optional[str], optional): summary docstring. Defaults to None.

        Raises:
            RoutePathExistsError: route with this path already exists
        """
        if methods is None:
            methods = ["GET"]

        page_path = page_path if self.prefix is None else f"{self.prefix}{page_path}"
        if page_path in self.routes:
            raise RoutePathExistsError(f'Route "{page_path}" already exists.')

        route = _create_page_route(
            page_path,
            handler,
            methods,
            summary,
        )

        if route.is_dynamic:
            self.dynamic_routes.append(route)
        else:
            self._trie.insert(page_path)

        self.routes[page_path] = route

    def add_url(self, url: URL):
        """Add a url

        Args:
            url (URL): URL class instance

        Raises:
            RoutePathExistsError: route with url.path already exists
        """
        url_path = url.path if self.prefix is None else f"{self.prefix}{url.path}"
        if url_path in self.routes:
            raise RoutePathExistsError(f'Route "{url_path}" already exists.')

        route = _create_url_route(url)

        if route.is_dynamic:
            self.dynamic_routes.append(route)
        else:
            self._trie.insert(url_path)

        self.routes[url_path] = route

    def resolve(
        self, request: Request, raise_404: Optional[bool] = True
    ) -> Union[Tuple[Callable, Dict], tuple[None, None]]:
        """Resolve path from request

        Args:
            request (Request): request object
            raise_404 (Optional[bool], optional): Raise 404 error if url not found or not. Defaults to True.

        Raises:
            URLNotFound: URL Not found, error 404

        Returns:
            Union[Tuple[Callable, Dict], tuple[None, None]]: route and parse result or none tuple
        """
        url = prepare_url(request.path)
        url = url if self.prefix is None else f"{self.prefix}{url}"

        # First try static routes using Trie
        if self._trie.find(url):
            if url in self.routes:
                return self.routes[url], {}

        # Check for static routes that might not be in Trie (fallback)
        elif url in self.routes and not self.routes[url].is_dynamic:
            return self.routes[url], {}

        # Then try dynamic routes
        for route in self.dynamic_routes:
            parse_result = parse.parse(route.page_path, url)
            if parse_result is not None:
                return route, parse_result.named

        if raise_404:
            raise URLNotFound(f'URL "{url}" not found.')
        else:
            return None, None
