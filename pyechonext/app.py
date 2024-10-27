import re
import inspect
from enum import Enum
from typing import Iterable, Callable, List, Type
from socks import method
from parse import parse
from pyechonext.urls import URL
from pyechonext.views import View
from pyechonext.request import Request
from pyechonext.response import Response
from pyechonext.utils.exceptions import RoutePathExistsError, MethodNotAllow
from pyechonext.utils import _prepare_url


class ApplicationType(Enum):
	JSON = "application/json"
	HTML = "text/html"


class EchoNext:
	"""
	This class describes an EchoNext WSGI Application.
	"""

	__slots__ = ("app_name", "application_type", "urls", "routes")

	def __init__(
		self,
		urls: List[URL],
		app_name: str,
		application_type: ApplicationType = ApplicationType.JSON,
	):
		"""
		Constructs a new instance.

		:param		app_name:  The application name
		:type		app_name:  str
		"""
		self.app_name = app_name
		self.application_type = application_type
		self.routes = {}
		self.urls = urls

	def _find_view(self, raw_url: str) -> Type[View]:
		url = _prepare_url(raw_url)

		for path in self.urls:
			match = re.match(path.url, url)

			if match is not None:
				return path

		return None

		# raise URLNotFound(f'URL "{raw_url}" not found.')

	def _check_request_method(self, view: View, request: Request):
		if not hasattr(view, request.method.lower()):
			raise MethodNotAllow(f"Method not allow: {request.method}")

	def _get_view(self, request: Request) -> View:
		url = request.path

		return self._find_view(url)()

	def _get_request(self, environ: dict) -> Request:
		return Request(environ)

	def _get_response(self) -> Response:
		return Response(content_type=self.application_type.value)

	def route_page(self, page_path: str) -> Callable:
		"""
		Creating a New Page Route

		:param		page_path:	The page path
		:type		page_path:	str

		:returns:	wrapper handler
		:rtype:		Callable
		"""
		if page_path in self.routes:
			raise RoutePathExistsError("Such route already exists.")

		def wrapper(handler):
			self.routes[page_path] = handler
			return handler

		return wrapper

	def default_response(self, response: Response) -> None:
		"""
		Get default response (404)

		:param		response:  The response
		:type		response:  Response
		"""
		response.status_code = "404"
		response.body = "Page Not Found Error."

	def find_handler(self, request_path: str) -> Callable:
		"""
		Finds a handler.

		:param		request_path:  The request path
		:type		request_path:  str

		:returns:	handler function
		:rtype:		Callable
		"""
		for path, handler in self.routes.items():
			parse_result = parse(path, request_path)
			if parse_result is not None:
				return handler, parse_result.named

		view = self._find_view(request_path)

		if view is not None:
			parse_result = parse(_prepare_url(view.url), request_path)
			if parse_result is not None:
				return view.view, parse_result.named

		return None, None

	def handle_response(self, request: Request) -> Response:
		"""
		Handle response from request

		:param		request:  The request
		:type		request:  Request

		:returns:	Response callable object
		:rtype:		Response
		"""
		response = self._get_response()

		handler, kwargs = self.find_handler(request_path=request.path)

		if handler is not None:
			if inspect.isclass(handler):
				handler = getattr(handler(), request.method.lower(), None)
				if handler is None:
					raise MethodNotAllow(f"Method not allowed: {request.method}")

			response.body = handler(request, response, **kwargs)
		else:
			self.default_response(response)

		return response

	def __call__(self, environ: dict, start_response: method) -> Iterable:
		"""
		Makes the application object callable

		:param		environ:		 The environ
		:type		environ:		 dict
		:param		start_response:	 The start response
		:type		start_response:	 method

		:returns:	response body
		:rtype:		Iterable
		"""
		request = self._get_request(environ)
		response = self.handle_response(request)

		return response(environ, start_response)
