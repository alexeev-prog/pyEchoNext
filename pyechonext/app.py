from enum import Enum
from typing import Iterable, Callable
from socks import method
from pyechonext.request import Request
from pyechonext.response import Response


class ApplicationType(Enum):
	JSON = 'application/json'
	HTML = 'text/html'


class EchoNext:
	"""
	This class describes an EchoNext WSGI Application.
	"""

	def __init__(self, app_name: str, application_type: ApplicationType=ApplicationType.JSON):
		"""
		Constructs a new instance.

		:param		app_name:  The application name
		:type		app_name:  str
		"""
		self.app_name = app_name
		self.application_type = application_type
		self.routes = {}

	def route_page(self, page_path: str) -> Callable:
		"""
		Creating a New Page Route

		:param		page_path:	The page path
		:type		page_path:	str

		:returns:	wrapper handler
		:rtype:		Callable
		"""

		def wrapper(handler):
			self.routes[page_path] = handler
			return handler

		return wrapper

	def default_response(self, response: Response) -> None:
		"""
		Get default response (404)

		:param      response:  The response
		:type       response:  Response
		"""
		response.status_code = "404"
		response.body = "Page Not Found Error."

	def handle_response(self, request: Request) -> Response:
		"""
		Handle response from request

		:param		request:  The request
		:type		request:  Request

		:returns:	Response callable object
		:rtype:		Response
		"""
		response = Response(content_type=self.application_type.value)

		handler = self.find_handler(request_path=request.path)

		if handler is not None:
			handler(request, response)
		else:
			self.default_response(response)

		return response

	def find_handler(self, request_path: str) -> Callable:
		"""
		Finds a handler.

		:param      request_path:  The request path
		:type       request_path:  str

		:returns:   handler function
		:rtype:     Callable
		"""
		for path, handler in self.routes.items():
			if path == request_path:
				return handler

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
		request = Request(environ)
		response = self.handle_response(request)

		return response(environ, start_response)
