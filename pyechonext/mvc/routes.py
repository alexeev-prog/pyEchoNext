from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, List, Optional, Tuple, Union

from parse import parse

from pyechonext.mvc.controllers import PageController
from pyechonext.request import Request
from pyechonext.urls import URL
from pyechonext.utils import _prepare_url
from pyechonext.utils.exceptions import RoutePathExistsError, URLNotFound


class RoutesTypes(Enum):
	"""
	This class describes routes types.
	"""

	URL_BASED = 0
	PAGE = 1


@dataclass
class Route:
	"""
	This class describes a route.
	"""

	page_path: str
	handler: Callable | PageController
	route_type: RoutesTypes
	summary: Optional[str] = None


def _create_url_route(url: URL) -> Route:
	"""
	Creates an url route.

	:param		url:  The url
	:type		url:  URL

	:returns:	Route dataclass object
	:rtype:		Route
	"""
	return Route(
		page_path=url.path,
		handler=url.controller(),
		route_type=RoutesTypes.URL_BASED,
		summary=url.summary,
	)


def _create_page_route(
	page_path: str, handler: Callable, summary: Optional[str] = None
) -> Route:
	"""
	Creates a page route.

	:param		page_path:	The page path
	:type		page_path:	str
	:param		handler:	The handler
	:type		handler:	Callable

	:returns:	Route dataclass object
	:rtype:		Route
	"""
	return Route(
		page_path=page_path,
		handler=handler,
		route_type=RoutesTypes.PAGE,
		summary=summary,
	)


class Router:
	"""
	This class describes a router.
	"""

	def __init__(self, urls: Optional[List[URL]] = []):
		"""
		Constructs a new instance.

		:param		urls:  The urls
		:type		urls:  Array
		"""
		self.urls = urls
		self.routes = {}

		self._prepare_urls()

	def _prepare_urls(self):
		"""
		Prepare URLs (add to routes)
		"""
		for url in self.urls:
			self.routes[url.path] = _create_url_route(url)

	def add_page_route(
		self, page_path: str, handler: Callable, summary: Optional[str] = None
	):
		"""
		Adds a page route.

		:param		page_path:			   The page path
		:type		page_path:			   str
		:param		handler:			   The handler
		:type		handler:			   Callable

		:raises		RoutePathExistsError:  Such route already exists
		"""
		if page_path in self.routes:
			raise RoutePathExistsError(f'Route "{page_path}" already exists.')

		self.routes[page_path] = _create_page_route(page_path, handler, summary)

	def generate_page_route(
		self, page_path: str, handler: Callable, summary: Optional[str] = None
	) -> Route:
		"""
		Generate page route

		:param		page_path:	The page path
		:type		page_path:	str
		:param		handler:	The handler
		:type		handler:	Callable

		:returns:	route dataclass object
		:rtype:		Route
		"""
		return _create_page_route(page_path, handler)

	def add_url(self, url: URL):
		"""
		Adds an url.

		:param		url:  The url
		:type		url:  URL
		"""
		if url.path in self.routes:
			raise RoutePathExistsError(f'Route "{url.path}" already exists.')

		self.routes[url.path] = _create_url_route(url)

	def resolve(
		self, request: Request, raise_404: Optional[bool] = True
	) -> Union[Tuple[Callable, Dict], None]:
		"""
		Resolve path from request

		:param		request:	  The request
		:type		request:	  Request
		:param		raise_404:	  Indicates if the 404 is raised
		:type		raise_404:	  bool

		:returns:	handler and named OR raise URLNotFound (if raise_404) OR None
		:rtype:		Union[Tuple[Callable, Dict], None]:

		:raises		URLNotFound:  URL Not Found
		"""
		url = _prepare_url(request.path)

		for path, route in self.routes.items():
			parse_result = parse(path, url)
			if parse_result is not None:
				return route, parse_result.named

		if raise_404:
			raise URLNotFound(f'URL "{url}" not found.')
		else:
			return None, None
