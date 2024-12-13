import inspect
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Iterable, List, Optional, Tuple, Type

from loguru import logger
from socks import method

from pyechonext.cache import InMemoryCache
from pyechonext.config import Settings
from pyechonext.i18n_l10n import JSONi18nLoader, JSONLocalizationLoader
from pyechonext.logging import setup_logger
from pyechonext.middleware import BaseMiddleware
from pyechonext.mvc.controllers import PageController
from pyechonext.mvc.routes import Router, RoutesTypes
from pyechonext.request import Request
from pyechonext.response import Response
from pyechonext.static import StaticFile, StaticFilesManager
from pyechonext.urls import URL
from pyechonext.utils import _prepare_url
from pyechonext.utils.exceptions import (
	MethodNotAllow,
	TeapotError,
	URLNotFound,
	WebError,
)
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
		"i18n_loader",
		"l10n_loader",
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
		"""
		Constructs a new instance.

		:param		app_name:		   The application name
		:type		app_name:		   str
		:param		settings:		   The settings
		:type		settings:		   Settings
		:param		middlewares:	   The middlewares
		:type		middlewares:	   List[BaseMiddleware]
		:param		urls:			   The urls
		:type		urls:			   List[URL]
		:param		application_type:  The application type
		:type		application_type:  ApplicationType
		:param		static_files:	   The static files
		:type		static_files:	   List[StaticFile]
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
		self.main_cache: InMemoryCache = InMemoryCache(timeout=60 * 10)
		self.history: List[HistoryEntry] = []
		self.i18n_loader: JSONi18nLoader = JSONi18nLoader(
			self.settings.LOCALE, self.settings.LOCALE_DIR
		)
		self.l10n_loader: JSONLocalizationLoader = JSONLocalizationLoader(
			self.settings.LOCALE, self.settings.LOCALE_DIR
		)

		if self.application_type == ApplicationType.TEAPOT:
			raise TeapotError("Where's my coffie?")

		setup_logger(self.app_name)

		logger.debug(f"Application {self.application_type.value}: {self.app_name}")

	def _get_request(self, environ: dict) -> Request:
		"""
		Gets the request.

		:param		environ:  The environ
		:type		environ:  dict

		:returns:	The request.
		:rtype:		Request
		"""
		return Request(environ, self.settings)

	def _get_response(self, request: Request) -> Response:
		"""
		Gets the response.

		:returns:	The response.
		:rtype:		Response
		"""
		return Response(request, content_type=self.application_type.value)

	def route_page(self, page_path: str) -> Callable:
		"""
		Creating a New Page Route

		:param		page_path:	The page path
		:type		page_path:	str

		:returns:	wrapper handler
		:rtype:		Callable
		"""

		def wrapper(handler):
			"""
			Wrapper for handler

			:param		handler:  The handler
			:type		handler:  callable

			:returns:	handler
			:rtype:		callable
			"""
			if inspect.isclass(handler):
				self.router.add_url(URL(path=page_path, controller=handler))
			else:
				self.router.add_page_route(page_path, handler)

			return handler

		return wrapper

	def _apply_middleware_to_request(self, request: Request):
		"""
		Apply middleware to request

		:param		request:  The request
		:type		request:  Request
		"""
		stack = LIFOStack()

		stack.push(*self.middlewares)

		for middleware in stack.items:
			middleware().to_request(request)

		while not stack.is_empty():
			stack.pop()

	def _apply_middleware_to_response(self, response: Response):
		"""
		Apply middleware to response

		:param		response:  The response
		:type		response:  Response
		"""
		stack = LIFOStack()

		stack.push(*self.middlewares)

		for middleware in stack.items:
			middleware().to_response(response)

		while not stack.is_empty():
			stack.pop()

	def _process_exceptions_from_middlewares(self, exception: Exception):
		stack = LIFOStack()

		stack.push(*self.middlewares)

		for middleware in stack.items:
			middleware().process_exception(exception)

		while not stack.is_empty():
			stack.pop()

	def _default_response(self, response: Response, error: WebError) -> None:
		"""
		Get default response (404)

		:param		response:  The response
		:type		response:  Response
		"""
		response.status_code = str(error.code)
		response.body = str(error)

	def _find_handler(self, request: Request) -> Tuple[Callable, str]:
		"""
		Finds a handler.

		:param		request_path:  The request path
		:type		request_path:  str

		:returns:	handler function and parsed result
		:rtype:		Tuple[Callable, str]
		"""
		url = _prepare_url(request.path)

		if self.static_files_manager.serve_static_file(url):
			return self.router.generate_page_route(url, self._serve_static_file), {}

		return self.router.resolve(request)

	def get_and_save_cache_item(self, key: str, value: Any) -> Any:
		"""
		Gets and save cached key.

		:param		key:	The key
		:type		key:	str
		:param		value:	The value
		:type		value:	Any

		:returns:	And save cached key.
		:rtype:		Any
		"""
		item = self.main_cache.get(key)

		if item is None:
			logger.info(f"Save item to cache: '{key[:16].strip()}...'")
			self.main_cache.set(key, value)
			item = self.main_cache.get(key)

		logger.info(f"Get item from cache: '{key[:16].strip()}...'")

		return item

	def _serve_static_file(
		self, request: Request, response: Response, **kwargs
	) -> Response:
		"""
		Serve static files

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary

		:returns:	response
		:rtype:		Response
		"""
		print(f"Serve static file by path: {request.path}")
		response.content_type = self.static_files_manager.get_file_type(request.path)
		response.body = self.static_files_manager.serve_static_file(
			_prepare_url(request.path)
		)
		return response

	def _handle_request(self, request: Request) -> Response:
		"""
		Handle response from request

		:param		request:  The request
		:type		request:  Request

		:returns:	Response callable object
		:rtype:		Response
		"""
		logger.debug(f"Handle request: {request.path}")
		response = self._get_response(request)

		route, kwargs = self._find_handler(request)

		handler = route.handler

		if handler is not None:
			if isinstance(handler, PageController) or inspect.isclass(handler):
				handler = getattr(handler, request.method.lower(), None)

				if handler is None:
					raise MethodNotAllow(
						f'Method "{request.method.lower()}" don\'t allowed: {request.path}'
					)

			result = handler(request, response, **kwargs)

			if isinstance(result, Response):
				result = result.body

			if route.route_type == RoutesTypes.URL_BASED:
				view = route.handler.get_rendered_view(request, result, self)
				response.body = view
			else:
				string = self.i18n_loader.get_string(result)
				response.body = self.get_and_save_cache_item(string, string)
		else:
			raise URLNotFound(f'URL "{request.path}" not found.')

		return response

	def switch_locale(self, locale: str, locale_dir: str):
		"""
		Switch to another locale i18n

		:param		locale:		 The locale
		:type		locale:		 str
		:param		locale_dir:	 The locale dir
		:type		locale_dir:	 str
		"""
		logger.info(f"Switch to another locale: {locale_dir}/{locale}")
		self.i18n_loader.locale = locale
		self.i18n_loader.directory = locale_dir
		self.i18n_loader.translations = self.i18n_loader.load_locale(
			self.i18n_loader.locale, self.i18n_loader.directory
		)
		self.l10n_loader.locale = locale
		self.l10n_loader.directory = locale_dir
		self.i18n_loader.locale_settings = self.l10n_loader.load_locale(
			self.l10n_loader.locale, self.l10n_loader.directory
		)

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
		self._apply_middleware_to_request(request)
		response = self._get_response(request)

		try:
			response = self._handle_request(request)
			self._apply_middleware_to_response(response)
		except URLNotFound as err:
			logger.error(
				"URLNotFound error has been raised: set default response (404)"
			)
			self._apply_middleware_to_response(response)
			self._default_response(response, error=err)
		except MethodNotAllow as err:
			logger.error(
				"MethodNotAllow error has been raised: set default response (405)"
			)
			self._apply_middleware_to_response(response)
			self._default_response(response, error=err)
		except Exception as ex:
			self._process_exceptions_from_middlewares(ex)

		self.history.append(HistoryEntry(request=request, response=response))
		return response(environ, start_response)
