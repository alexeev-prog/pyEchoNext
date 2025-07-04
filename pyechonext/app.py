import inspect
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Iterable, List, Optional, Type

from requests import Session as RequestsSession
from socks import method
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

from pyechonext.cache import InMemoryCache
from pyechonext.config import Settings
from pyechonext.logging import logger
from pyechonext.middleware import BaseMiddleware
from pyechonext.mvc.controllers import PageController
from pyechonext.mvc.routes import (Route, Router, RoutesTypes,
                                   generate_page_route)
from pyechonext.request import Request
from pyechonext.response import Response
from pyechonext.static import StaticFile, StaticFilesManager
from pyechonext.urls import URL
from pyechonext.utils import prepare_url
from pyechonext.utils.exceptions import (MethodNotAllow, RoutePathExistsError,
                                         TeapotError, URLNotFound, WebError)
from pyechonext.utils.stack import LIFOStack


class ApplicationType(Enum):
    """
    This enum class describes an application type.
    """

    JSON = "application/json"
    HTML = "text/html"
    PLAINTEXT = "text/plain"
    TEAPOT = "server/teapot"


@dataclass
class HistoryEntry:
    request: Request
    response: Response


def _default_response(response: Response, error: WebError) -> None:
    """Get default response (HTTP 404)

    Args:
        response (Response): Response object
        error (WebError): web error
    """
    response.status_code = str(error.code)
    response.body = str(error)


def _check_handler(request: Request, route: Route) -> Callable:
    """Check handler

    Args:
        request (Request): request object
        route (Route): route

    Raises:
        MethodNotAllow: handler request method is None, method not allowed

    Returns:
        Callable: handler object
    """
    handler = route.handler

    if isinstance(handler, PageController) or inspect.isclass(handler):
        handler = getattr(handler, request.method.lower(), None)

        if handler is None:
            raise MethodNotAllow(
                f'Method "{request.method.lower()}" don\'t allowed: {request.path}'
            )
    elif route.route_type == RoutesTypes.PAGE:
        method = request.method.upper()

        if method not in route.methods:
            raise MethodNotAllow(
                f'Method "{request.method.lower()}" don\'t allowed: {request.path}'
            )

    return handler


class EchoNext:
    """
    This class describes an EchoNext WSGI Application.
    """

    __slots__ = (
        "app_name",
        "settings",
        "middlewares",
        "application_type",
        "urls",
        "router",
        "_included_routers",
        "history",
        "main_cache",
        "static_files_manager",
        "static_files",
    )

    def __init__(
        self,
        app_name: str,
        settings: Settings,
        middlewares: List[Type[BaseMiddleware]],
        urls: Optional[List[URL]] = [],
        application_type: Optional[ApplicationType] = ApplicationType.JSON,
        static_files: Optional[List[StaticFile]] = [],
    ):
        """Initialize a WSGI

        Args:
            app_name (str): application name
            settings (Settings): settings of app            middlewares (List[Type[BaseMiddleware]]): list of middlewares
            urls (Optional[List[URL]], optional): basic URLs list. Defaults to [].
            application_type (Optional[ApplicationType], optional): application type. Defaults to ApplicationType.JSON.
            static_files (Optional[List[StaticFile]], optional): static files list. Defaults to [].

        Raises:
            TeapotError: Easter Egg
        """
        self.app_name: str = app_name
        self.settings: Settings = settings
        self.middlewares: List[Type[BaseMiddleware]] = middlewares
        self.application_type: ApplicationType = application_type
        self.static_files: List[StaticFile] = static_files
        self.static_files_manager: StaticFilesManager = StaticFilesManager(
            self.static_files
        )
        self.urls: List[URL] = urls
        self.router: Router = Router(self.urls)
        self._included_routers: List[Router] = []
        self.main_cache: InMemoryCache = InMemoryCache(timeout=60 * 10)
        self.history: List[HistoryEntry] = []

        if self.application_type == ApplicationType.TEAPOT:
            raise TeapotError("Where's my coffee?")

        logger.debug(
            f"Application {self.application_type.value}: {self.app_name}")

    def test_session(self, host: str = "echonext") -> RequestsSession:
        """Test Session

        Args:
            host (str, optional): hostname of session. Defaults to "echonext".

        Returns:
            RequestsSession: request session for tests
        """
        session = RequestsSession()
        session.mount(prefix=f"http://{host}",
                      adapter=RequestsWSGIAdapter(self))
        return session

    def _get_request(self, environ: dict) -> Request:
        """Get request object

        Args:
            environ (dict): environ info

        Returns:
            Request: request object
        """
        return Request(environ, self.settings)

    def _get_response(self, request: Request) -> Response:
        """Get response object

        Args:
            request (Request): basic request

        Returns:
            Response: response object
        """
        return Response(request, content_type=self.application_type.value)

    def add_route(
        self,
        page_path: str,
        handler: Callable | PageController,
        methods: Optional[List[str]] = None,
        summary: Optional[str] = None,
    ):
        """Add page route without decorator

        Args:
            page_path (str): page path url
            handler (Callable): handler of route
            methods (Optional[List[str]]): supported methods of handler. Defaults to None.
            summary (Optional[str], optional): summary documentation. Defaults to None.
        """
        if methods is None:
            methods = ["GET"]
        if inspect.isclass(handler):
            self.router.add_url(URL(path=page_path, controller=handler))
        else:
            self.router.add_page_route(page_path, handler, methods, summary)

    def route_page(
        self,
        page_path: str,
        methods: Optional[List[str]] = None,
        summary: Optional[str] = None,
    ) -> Callable:
        """Route page decorator

        Args:
            page_path (str): page path url
            methods (Optional[List[str]]): supported methods of handler. Defaults to None.
            summary (Optional[str], optional): summary documentation. Defaults to None.

        Returns:
            Callable: wrapper
        """

        if methods is None:
            methods = ["GET"]

        def wrapper(handler: Callable | PageController):
            if inspect.isclass(handler):
                self.router.add_url(
                    URL(path=page_path, controller=handler, summary=summary)
                )
            else:
                self.router.add_page_route(
                    page_path,
                    handler,
                    methods,
                    summary,
                )

            return handler

        return wrapper

    def _apply_middlewares_to_request(self, request: Request):
        """Apply middlewares to request

        Args:
            request (Request): request for applying middlewares
        """
        stack = LIFOStack()

        stack.push(*self.middlewares)

        for middleware in stack.items:
            middleware().to_request(request)

        while not stack.is_empty():
            stack.pop()

    def _apply_middlewares_to_response(self, response: Response):
        """Apply middlewares to response

        Args:
            response (Response): request for applying middlewares
        """
        stack = LIFOStack()

        stack.push(*self.middlewares)

        for middleware in stack.items:
            middleware().to_response(response)

        while not stack.is_empty():
            stack.pop()

    def _process_exceptions_from_middlewares(self, exception: Exception):
        """Process exceptions from middlewares

        Args:
            exception (Exception): exception class
        """
        stack = LIFOStack()

        stack.push(*self.middlewares)

        for middleware in stack.items:
            middleware().process_exception(exception)

        while not stack.is_empty():
            stack.pop()

    def include_router(self, new_router: Router):
        """Include new router to additional routers list

        Args:
            new_router (Router): new router object
        """
        new_router_routes = [path for path, _ in new_router.routes.items()]
        old_router_routes = [path for path, _ in self.router.routes.items()]

        if len(set(old_router_routes).intersection(new_router_routes)) == 0:
            for included_router in self._included_routers:
                if set(
                    [path for path, _ in included_router.routes.items()]
                ).intersection(new_router_routes):
                    raise RoutePathExistsError(
                        "Next router paths already exists:"
                        f" {set(included_router.routes).intersection(new_router_routes)}"
                    )

            self._included_routers.append(new_router)
            return

        raise RoutePathExistsError(
            "Next router paths already exists:"
            f" {set(old_router_routes).intersection(new_router_routes)}"
        )

    def _find_handler(
        self, request: Request
    ) -> tuple[Any, Any] | tuple[Route, dict[Any, Any]]:
        """Find handler by request

        Args:
            request (Request): Request object

        Returns:
            Tuple[Callable, str]: handlers tuple
        """
        url = prepare_url(request.path)

        if self.static_files_manager.serve_static_file(url):
            return (
                generate_page_route(
                    url, self._serve_static_file, None, f"Serving static file: {url}"
                ),
                {},
            )

        route, parse_result = self.router.resolve(request, raise_404=False)

        if route is None and parse_result is None:
            for router in self._included_routers:
                route, parse_result = router.resolve(request, raise_404=False)
                if route is not None and parse_result is not None:
                    return route, parse_result

        if route is None and parse_result is None:
            raise URLNotFound(f'URL "{url}" not found')

        return route, parse_result

    def get_and_save_cache_item(self, key: str, value: Any) -> Any:
        """Set and save item to cache

        Args:
            key (str): key
            value (Any): value

        Returns:
            Any: item from cache
        """
        key = str(key)
        item = self.main_cache.get(key)
        cache_key = key[:16].strip().replace('\n', '')

        if item is None:
            logger.info(
                f"Save item to cache: '{cache_key}...'"
            )
            self.main_cache.set(key, value)
            item = self.main_cache.get(key)

        logger.info(
            f"Get item from cache: '{cache_key}...'")

        return item

    def _serve_static_file(
        self, request: Request, response: Response, **kwargs
    ) -> Response:
        """Serve static files

        Args:
            request (Request): request object
            response (Response): response object

        Returns:
            Response: served response object
        """
        logger.debug(f"Serve static file by path: {request.path}")
        response.content_type = self.static_files_manager.get_file_type(
            request.path)
        response.body = self.static_files_manager.serve_static_file(
            prepare_url(request.path)
        )
        return response

    def _filling_response(
        self,
        route: Route,
        response: Response,
        request: Request,
        result: Any,
        handler: Callable,
    ):
        """Filling response

        Args:
            route (Route): route
            response (Response): response object
            request (Request): request object
            result (Any): result data
            handler (Callable): handler object
        """
        if route.route_type == RoutesTypes.URL_BASED:
            view = route.handler.get_rendered_view(request, result)
            response.body = view
        else:
            response.body = self.get_and_save_cache_item(result, result)

    def _handle_request(self, request: Request) -> Response:
        """Handle request

        Args:
            request (Request): request object

        Raises:
            URLNotFound: URL for request not found

        Returns:
            Response: response object
        """
        logger.debug(f"Handle request: {request.path}")
        response = self._get_response(request)

        route, kwargs = self._find_handler(request)

        handler = route.handler

        if handler is not None:
            handler = _check_handler(request, route)

            result = handler(request, response, **kwargs)

            if isinstance(result, Response):
                result = result.body
            elif result is None:
                return response

            self._filling_response(route, response, request, result, handler)
        else:
            raise URLNotFound(f'URL "{request.path}" not found.')

        return response

    def __call__(self, environ: dict, start_response: method) -> Iterable:
        """Makes the application object callable

        Args:
            environ (dict): environ dictionary
            start_response (method): the start response

        Returns:
            Iterable: iterable response
        """
        request = self._get_request(environ)
        self._apply_middlewares_to_request(request)
        response = self._get_response(request)

        try:
            response = self._handle_request(request)
            self._apply_middlewares_to_response(response)
        except URLNotFound as err:
            logger.error(
                "URLNotFound error has been raised: set default response (404)"
            )
            self._apply_middlewares_to_response(response)
            _default_response(response, error=err)
        except MethodNotAllow as err:
            logger.error(
                "MethodNotAllow error has been raised: set default response (405)"
            )
            self._apply_middlewares_to_response(response)
            _default_response(response, error=err)
        except Exception as ex:
            self._process_exceptions_from_middlewares(ex)

        self.history.append(HistoryEntry(request=request, response=response))
        return response(environ, start_response)
