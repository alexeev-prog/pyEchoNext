import inspect
from enum import Enum
from typing import Iterable, Callable, List, Type, Tuple, Optional, Union, Any
from dataclasses import dataclass
from socks import method
from parse import parse
from loguru import logger
from pyechonext.urls import URL
from pyechonext.views import View
from pyechonext.request import Request
from pyechonext.response import Response
from pyechonext.utils.exceptions import (
	RoutePathExistsError,
	MethodNotAllow,
	URLNotFound,
	WebError,
	TeapotError,
)
from pyechonext.utils import _prepare_url
from pyechonext.config import Settings
from pyechonext.middleware import BaseMiddleware
from pyechonext.i18n_l10n.i18n import JSONi18nLoader
from pyechonext.i18n_l10n.l10n import JSONLocalizationLoader
from pyechonext.logging import setup_logger
from pyechonext.cache import InMemoryCache


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
		"routes",
		"i18n_loader",
		"l10n_loader",
		"history",
		"main_cache",
	)

	def __init__(
		self,
		app_name: str,
		settings: Settings,
		middlewares: List[Type[BaseMiddleware]],
		urls: Optional[List[URL]] = [],
		application_type: Optional[ApplicationType] = ApplicationType.JSON,
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
		:type		application_type:  Optional[ApplicationType]
		"""
		self.app_name = app_name
		self.settings = settings
		self.middlewares = middlewares
		self.application_type = application_type
		self.routes = {}
		self.urls = urls
		self.main_cache = InMemoryCache(timeout=60 * 10)
		self.history: List[HistoryEntry] = []
		self.i18n_loader = JSONi18nLoader(
			self.settings.LOCALE, self.settings.LOCALE_DIR
		)
		self.l10n_loader = JSONLocalizationLoader(
			self.settings.LOCALE, self.settings.LOCALE_DIR
		)
		logger.debug(f"Application {self.application_type.value}: {self.app_name}")

		if self.application_type == ApplicationType.TEAPOT:
			raise TeapotError("Where's my coffie?")

		setup_logger(self.app_name)

	def _find_view(self, raw_url: str) -> Union[Type[URL], None]:
		"""
		Finds a view by raw url.

		:param		raw_url:  The raw url
		:type		raw_url:  str

		:returns:	URL dataclass
		:rtype:		Type[URL]
		"""
		url = _prepare_url(raw_url)

		for path in self.urls:
			if url == _prepare_url(path.url):
				return path

		return None

	def _check_request_method(self, view: View, request: Request):
		"""
		Check request method for view

		:param		view:			 The view
		:type		view:			 View
		:param		request:		 The request
		:type		request:		 Request

		:raises		MethodNotAllow:	 Method not allow
		"""
		if not hasattr(view, request.method.lower()):
			raise MethodNotAllow(f"Method not allow: {request.method}")

	def _get_view(self, request: Request) -> View:
		"""
		Gets the view.

		:param		request:  The request
		:type		request:  Request

		:returns:	The view.
		:rtype:		View
		"""
		url = request.path

		return self._find_view(url)

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
		if page_path in self.routes:
			raise RoutePathExistsError("Such route already exists.")

		def wrapper(handler):
			"""
			Wrapper for handler

			:param		handler:  The handler
			:type		handler:  callable

			:returns:	handler
			:rtype:		callable
			"""
			self.routes[page_path] = handler
			return handler

		return wrapper

	def _apply_middleware_to_request(self, request: Request):
		"""
		Apply middleware to request

		:param		request:  The request
		:type		request:  Request
		"""
		for middleware in self.middlewares:
			middleware().to_request(request)

	def _apply_middleware_to_response(self, response: Response):
		"""
		Apply middleware to response

		:param		response:  The response
		:type		response:  Response
		"""
		for middleware in self.middlewares:
			middleware().to_response(response)

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

		for path, handler in self.routes.items():
			parse_result = parse(path, url)
			if parse_result is not None:
				return handler, parse_result.named

		view = self._get_view(request)

		if view is not None:
			parse_result = parse(view.url, url)

			if parse_result is not None:
				return view.view, parse_result.named

		return None, None

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
			logger.info(f"Save item to cache: {key}={str(value)[:32]}")
			self.main_cache.set(key, value)
			item = self.main_cache.get(key)

		logger.info(f"Get item from cache: {key}: {item}")

		return item

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

		handler, kwargs = self._find_handler(request)

		if handler is not None:
			if inspect.isclass(handler):
				handler = getattr(handler(), request.method.lower(), None)
				if handler is None:
					raise MethodNotAllow(f"Method not allowed: {request.method}")

			result = handler(request, response, **kwargs)

			if isinstance(result, Response):
				response = result

				if response.use_i18n:
					response.body = self.i18n_loader.get_string(
						response.body, **response.i18n_kwargs
					)
			else:
				string = self.i18n_loader.get_string(result)
				response.body = self.get_and_save_cache_item(string, string)

				if not response.use_i18n:
					response.body = self.get_and_save_cache_item(result, result)
		else:
			raise URLNotFound(f'URL "{request.path}" not found.')

		response = self.get_and_save_cache_item(str(response), response)

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

		self.history.append(HistoryEntry(request=request, response=response))
		return response(environ, start_response)
