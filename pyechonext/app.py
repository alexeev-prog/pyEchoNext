import inspect
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Iterable, List, Optional, Tuple, Type

from loguru import logger
from requests import Session as RequestsSession
from socks import method
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

from pyechonext.cache import InMemoryCache
from pyechonext.config import Settings
from pyechonext.i18n_l10n import JSONi18nLoader, JSONLocalizationLoader
from pyechonext.logging import setup_logger
from pyechonext.middleware import BaseMiddleware
from pyechonext.mvc.controllers import PageController
from pyechonext.mvc.routes import Route, Router, RoutesTypes
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
		"""Initialize a WSGI

		Args:
				app_name (str): application name
				settings (Settings): settings of app
				middlewares (List[Type[BaseMiddleware]]): list of middlewares
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
		self.main_cache: InMemoryCache = InMemoryCache(timeout=60 * 10)
		self.history: List[HistoryEntry] = []
		self.i18n_loader: JSONi18nLoader = JSONi18nLoader(
			self.settings.LOCALE, self.settings.LOCALE_DIR
		)
		self.l10n_loader: JSONLocalizationLoader = JSONLocalizationLoader(
			self.settings.LOCALE, self.settings.LOCALE_DIR
		)

		self._validate_arguments()	# Validate arguments

		if self.application_type == ApplicationType.TEAPOT:
			raise TeapotError("Where's my coffie?")

		setup_logger(self.app_name)

		logger.debug(f"Application {self.application_type.value}: {self.app_name}")

	def _validate_arguments(self):
		"""Validate arguments and params at app initialization

		Raises:
				ValueError: _description_
		"""
		# Check URLs
		for url in self._urls:
			if not isinstance(url.controller, PageController):
				raise ValueError(
					f"URL Controller {url.path} must be PageController, not {type(url.controller)}"
				)

	def test_session(self, host: str = "echonext") -> RequestsSession:
		"""Test Session

		Args:
						host (str, optional): hostname of session. Defaults to "echonext".

		Returns:
						RequestsSession: request session for tests
		"""
		session = RequestsSession()
		session.mount(prefix=f"http://{host}", adapter=RequestsWSGIAdapter(self))
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
		self, page_path: str, handler: Callable, summary: Optional[str] = None
	):
		"""Add page route

		Args:
				page_path (str): page path url
				handler (Callable): handler of route
				summary (Optional[str], optional): summary documentation. Defaults to None.
		"""
		if inspect.isclass(handler):
			self.router.add_url(URL(path=page_path, controller=handler))
		else:
			self.router.add_page_route(page_path, handler, summary)

	def route_page(self, page_path: str, summary: Optional[str] = None) -> Callable:
		"""Route page

		Args:
				page_path (str): page path url
				summary (Optional[str], optional): summary documentation. Defaults to None.

		Returns:
				Callable: wrapper
		"""

		def wrapper(handler):
			"""Decoration for page routing.

			Args:
					handler (_type_): handler function

			Returns:
					_type_: handler function
			"""
			if inspect.isclass(handler):
				self.router.add_url(
					URL(path=page_path, controller=handler, summary=summary)
				)
			else:
				self.router.add_page_route(page_path, handler, summary)

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

	def _default_response(self, response: Response, error: WebError) -> None:
		"""Get default response (HTTP 404)

		Args:
				response (Response): Response object
				error (WebError): web error
		"""
		response.status_code = str(error.code)
		response.body = str(error)

	def _find_handler(self, request: Request) -> Tuple[Callable, str]:
		"""Find handler by request

		Args:
				request (Request): Request object

		Returns:
				Tuple[Callable, str]: handlers tuple
		"""
		url = _prepare_url(request.path)

		if self.static_files_manager.serve_static_file(url):
			return (
				self.router.generate_page_route(
					url, self._serve_static_file, f"Serving static file: {url}"
				),
				{},
			)

		return self.router.resolve(request)

	def get_and_save_cache_item(self, key: str, value: Any) -> Any:
		"""Set and save item to cache

		Args:
				key (str): key
				value (Any): value

		Returns:
				Any: item from cache
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
		"""Serve static files

		Args:
				request (Request): request object
				response (Response): response object

		Returns:
				Response: served response object
		"""
		logger.debug(f"Serve static file by path: {request.path}")
		response.content_type = self.static_files_manager.get_file_type(request.path)
		response.body = self.static_files_manager.serve_static_file(
			_prepare_url(request.path)
		)
		return response

	def _check_handler(self, request: Request, handler: Callable) -> Callable:
		"""Check handler

		Args:
				request (Request): request object
				handler (Callable): handler

		Raises:
				MethodNotAllow: handler request method is None, method not allowed

		Returns:
				Callable: _description_
		"""
		if isinstance(handler, PageController) or inspect.isclass(handler):
			handler = getattr(handler, request.method.lower(), None)

			if handler is None:
				raise MethodNotAllow(
					f'Method "{request.method.lower()}" don\'t allowed: {request.path}'
				)

		return handler

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
			view = route.handler.get_rendered_view(request, result, self)
			response.body = view
		else:
			string = self.i18n_loader.get_string(result)
			response.body = self.get_and_save_cache_item(string, string)

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
			handler = self._check_handler(request, handler)

			result = handler(request, response, **kwargs)

			if isinstance(result, Response):
				result = result.body
			elif result is None:
				return response

			self._filling_response(route, response, request, result, handler)
		else:
			raise URLNotFound(f'URL "{request.path}" not found.')

		return response

	def switch_locale(self, locale: str, locale_dir: str):
		"""Switch locale

		Args:
				locale (str): locale name
				locale_dir (str): directory with locales
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
			self._default_response(response, error=err)
		except MethodNotAllow as err:
			logger.error(
				"MethodNotAllow error has been raised: set default response (405)"
			)
			self._apply_middlewares_to_response(response)
			self._default_response(response, error=err)
		except Exception as ex:
			self._process_exceptions_from_middlewares(ex)

		self.history.append(HistoryEntry(request=request, response=response))
		return response(environ, start_response)
