from typing import Callable, Optional, List, Tuple, Dict, Union
from enum import Enum
from dataclasses import dataclass
from parse import parse
# from pyechonext.mvc.controllers import BaseController
from pyechonext.views import View
from pyechonext.urls import URL
from pyechonext.utils.exceptions import RoutePathExistsError
from pyechonext.request import Request
from pyechonext.utils import _prepare_url
from pyechonext.utils.exceptions import (
	MethodNotAllow,
	RoutePathExistsError,
	TeapotError,
	URLNotFound,
	WebError,
)


class RoutesTypes(Enum):
	"""
	This class describes routes types.
	"""

	URL = 0
	PAGE = 1


@dataclass
class Route:
	"""
	This class describes a route.
	"""

	page_path: str
	handler: Callable | View
	route_type: RoutesTypes


def _create_url_route(url: URL) -> Route:
	"""
	Creates an url route.

	:param      url:  The url
	:type       url:  URL

	:returns:   Route dataclass object
	:rtype:     Route
	"""
	return Route(page_path=url.url, handler=url.view, route_type=RoutesTypes.URL)


def _create_page_route(page_path: str, handler: Callable) -> Route:
	"""
	Creates a page route.

	:param      page_path:  The page path
	:type       page_path:  str
	:param      handler:    The handler
	:type       handler:    Callable

	:returns:   Route dataclass object
	:rtype:     Route
	"""
	return Route(page_path=page_path, handler=handler, route_type=RoutesTypes.PAGE)


class Router:
	"""
	This class describes a router.
	"""

	def __init__(self, urls: Optional[List[URL]] = []):
		"""
		Constructs a new instance.

		:param      urls:  The urls
		:type       urls:  Array
		"""
		self.urls = urls
		self.routes = {}

		self._prepare_urls()

	def _prepare_urls(self):
		"""
		Prepare URLs (add to routes)
		"""
		for url in self.urls:
			self.routes[url.url] = _create_url_route(url)

	def add_page_route(self, page_path: str, handler: Callable):
		"""
		Adds a page route.

		:param      page_path:             The page path
		:type       page_path:             str
		:param      handler:               The handler
		:type       handler:               Callable

		:raises     RoutePathExistsError:  Such route already exists
		"""
		if page_path in self.routes:
			raise RoutePathExistsError(f'Route "{page_path}" already exists.')

		self.routes[page_path] = _create_page_route(page_path, handler)

	def add_url(self, url: URL):
		"""
		Adds an url.

		:param      url:  The url
		:type       url:  URL
		"""
		self.routes[url.url] = _create_url_route(url)

	def resolve(self, request: Request, raise_404: Optional[bool] = True) -> Union[Tuple[Callable, Dict], None]:
		"""
		Resolve path from request

		:param      request:      The request
		:type       request:      Request
		:param      raise_404:    Indicates if the 404 is raised
		:type       raise_404:    bool

		:returns:   handler and named OR raise URLNotFound (if raise_404) OR None
		:rtype:     Union[Tuple[Callable, Dict], None]:

		:raises     URLNotFound:  URL Not Found
		"""
		url = _prepare_url(request.path)

		for path, route in self.routes.items():
			parse_result = parse(path, url)
			if parse_result is not None:
				return route.handler, parse_result.named

		if raise_404:
			raise URLNotFound(f'URL "{url}" not found.')
		else:
			return None, None
