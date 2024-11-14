# pyEchoNext / Request/Response

---

Request - HTTP-запрос. Response - HTTP-ответ.

## Введение
В информатике запрос-ответ или запрос-реплика - это один из основных методов, используемых компьютерами для связи друг с другом в сети, при котором первый компьютер отправляет запрос на некоторые данные, а второй отвечает на запрос. Более конкретно, это шаблон обмена сообщениями, при котором запрашивающий отправляет сообщение с запросом системе-ответчику, которая получает и обрабатывает запрос, в конечном счете возвращая сообщение в ответ. Это аналогично телефонному звонку, при котором вызывающий абонент должен дождаться, пока получатель возьмет трубку, прежде чем что-либо можно будет обсудить.

## Request
**Request** — это запрос, который содержит данные для взаимодействия между клиентом и API: базовый URL, конечную точку, используемый метод, заголовки и т. д..

```python
class Request:
	"""
	This class describes a request.
	"""

	def __init__(self, environ: dict, settings: Settings):
		"""
		Constructs a new instance.

		:param		environ:  The environ
		:type		environ:  dict
		"""
		self.environ: dict = environ
		self.settings: Settings = settings
		self.method: str = self.environ["REQUEST_METHOD"]
		self.path: str = self.environ["PATH_INFO"]
		self.GET: dict = self._build_get_params_dict(self.environ["QUERY_STRING"])
		self.POST: dict = self._build_post_params_dict(self.environ["wsgi.input"].read())
		self.user_agent: str = self.environ["HTTP_USER_AGENT"]
		self.extra: dict = {}

		logger.debug(f"New request created: {self.method} {self.path}")

	def __getattr__(self, item: Any) -> Union[Any, None]:
		"""
		Magic method for get attrs (from extra)

		:param		item:  The item
		:type		item:  Any

		:returns:	Item from self.extra or None
		:rtype:		Union[Any, None]
		"""
		return self.extra.get(item, None)

	def _build_get_params_dict(self, raw_params: str):
		"""
		Builds a get parameters dictionary.

		:param		raw_params:	 The raw parameters
		:type		raw_params:	 str
		"""
		return parse_qs(raw_params)

	def _build_post_params_dict(self, raw_params: bytes):
		"""
		Builds a post parameters dictionary.

		:param		raw_params:	 The raw parameters
		:type		raw_params:	 bytes
		"""
		return parse_qs(raw_params.decode())
```

Request требует следующие аргументы для создания:

 + environ (словарь) - веб-окружение (генерируется gunicorn)
 + settings (объект датакласса pyechonext.config.Settings)

Request имеет следующие публичные атрибуты:

 + environ (словарь) - веб-окружение
 + settings (объект датакласса pyechonext.config.Settings)
 + method (строка) - http-метод
 + path (строка) - путь
 + GET (словарь) - параметры get-запроса
 + POST (словарь) - параметры post-запроса
 + user_agent (строка) - User-Agent
 + extra (словарь) - дополнительные параметры (например для middleware)

Request также имеет следующие методы:
 
 + `__getattr__` - магический метод дескриптора для получения атрибутов (для получения элементов из атрибута extra)
 + `_build_get_params_dict` - приватный метод для парсинга параметров get-запроса
 + `_build_post_params_dict` - приватный метод для парсинга параметров post-запроса

## Response
**Response** — это ответ, который содержит данные, возвращаемые сервером, в том числе контент, код состояния и заголовки.

```python
import json
from typing import Dict, Iterable, Union, Any, List, Tuple, Optional
from socks import method
from loguru import logger
from pyechonext.request import Request


class Response:
	"""
	This dataclass describes a response.
	"""

	default_content_type: str = "text/html"
	default_charset: str = "UTF-8"
	unicode_errors: str = "strict"
	default_conditional_response: bool = False
	default_body_encoding: str = "UTF-8"

	def __init__(
		self,
		request: Request,
		use_i18n: bool = False,
		status_code: Optional[int] = 200,
		body: Optional[str] = None,
		headers: Optional[Dict[str, str]] = {},
		content_type: Optional[str] = None,
		charset: Optional[str] = None,
		**kwargs,
	):
		"""
		Constructs a new instance.

		:param		request:	   The request
		:type		request:	   Request
		:param		use_i18n:	   The use i 18 n
		:type		use_i18n:	   bool
		:param		status_code:   The status code
		:type		status_code:   int
		:param		body:		   The body
		:type		body:		   str
		:param		headers:	   The headers
		:type		headers:	   Dict[str, str]
		:param		content_type:  The content type
		:type		content_type:  str
		:param		charset:	   The charset
		:type		charset:	   str
		:param		kwargs:		   The keywords arguments
		:type		kwargs:		   dictionary
		"""
		if status_code == 200:
			self.status_code: str = "200 OK"
		else:
			self.status_code: str = str(status_code)

		if content_type is None:
			self.content_type: str = self.default_content_type
		else:
			self.content_type: str = content_type

		if charset is None:
			self.charset: str = self.default_charset
		else:
			self.charset: str = charset

		if body is not None:
			self.body: str = body
		else:
			self.body: str = ""

		self._headerslist: list = headers
		self._added_headers: list = []
		self.request: Request = request
		self.extra: dict = {}

		self.use_i18n: bool = use_i18n
		self.i18n_kwargs = kwargs

		self._update_headers()

	def __getattr__(self, item: Any) -> Union[Any, None]:
		"""
		Magic method for get attrs (from extra)

		:param		item:  The item
		:type		item:  Any

		:returns:	Item from self.extra or None
		:rtype:		Union[Any, None]
		"""
		return self.extra.get(item, None)

	def _structuring_headers(self, environ):
		headers = {
			"Host": environ["HTTP_HOST"],
			"Accept": environ["HTTP_ACCEPT"],
			"User-Agent": environ["HTTP_USER_AGENT"],
		}

		for name, value in headers.items():
			self._headerslist.append((name, value))

		for header_tuple in self._added_headers:
			self._headerslist.append(header_tuple)

	def _update_headers(self) -> None:
		"""
		Sets the headers by environ.

		:param		environ:  The environ
		:type		environ:  dict
		"""
		self._headerslist = [
			("Content-Type", f"{self.content_type}; charset={self.charset}"),
			("Content-Length", str(len(self.body))),
		]

	def add_headers(self, headers: List[Tuple[str, str]]):
		"""
		Adds new headers.

		:param		headers:  The headers
		:type		headers:  List[Tuple[str, str]]
		"""
		for header in headers:
			self._added_headers.append(header)

	def _encode_body(self):
		"""
		Encodes a body.
		"""
		if self.content_type.split("/")[-1] == "json":
			self.body = str(self.json)

		try:
			self.body = self.body.encode("UTF-8")
		except AttributeError:
			self.body = str(self.body).encode("UTF-8")

	def __call__(self, environ: dict, start_response: method) -> Iterable:
		"""
		Makes the Response object callable.

		:param		environ:		 The environ
		:type		environ:		 dict
		:param		start_response:	 The start response
		:type		start_response:	 method

		:returns:	response body
		:rtype:		Iterable
		"""
		self._encode_body()

		self._update_headers()
		self._structuring_headers(environ)

		logger.debug(
			f"[{environ['REQUEST_METHOD']} {self.status_code}] Run response: {self.content_type}"
		)

		start_response(status=self.status_code, headers=self._headerslist)

		return iter([self.body])

	@property
	def json(self) -> dict:
		"""
		Parse request body as JSON.

		:returns:	json body
		:rtype:		dict
		"""
		if self.body:
			if self.content_type.split("/")[-1] == "json":
				return json.dumps(self.body)
			else:
				return json.dumps(self.body.decode("UTF-8"))

		return {}

	def __repr__(self):
		"""
		Returns a unambiguous string representation of the object (for debug...).

		:returns:	String representation of the object.
		:rtype:		str
		"""
		return f"<{self.__class__.__name__} at 0x{abs(id(self)):x} {self.status_code}>"
```

Response имеет следующие аргументы:

 + request (объект класса Request) - запрос
 + [опционально] status_code (целочисленное значение) - статус-код ответа
 + [опционально] body (строка) - тело ответа
 + [опционально] headers (словарь) - заголовки ответа
 + [опционально] content_type (строка) - тип контента ответа
 + [опционально] charset (строка) - кодировка ответа
 + [опционально] use_i18n (логическое значение) - использовать ли i18n (по умолчанию False)

Response имеет следующие атрибуты:

 + status_code (строка) - статус-код (по умолчанию "200 OK")
 + content_type (строка) - контент-тип (по умолчанию равен значению default_content_type)
 + charset (строка) - кодировка (по умолчанию равен значению default_charset)
 + body (строка) - тело овтета (по умолчанию равен пустой строке)
 + `_headerslist` (список) - приватный список заголовков ответа
 + `_added_headers` (список) - приватный список добавленных заголовков ответа
 + request (объект класса Request) - запрос
 + extra (словарь) - дополнительные параметры

Response имеет следующие методы:

 + `__getattr__` - магический метод дескриптора для получения атрибутов (для получения элементов из атрибута extra)
 + `_structuring_headers` - приватный метод структуирования заголовков из веб-окружения
 + `_update_headers` - приватный метод обновления (перезаписывания) списков заголовков
 + `add_headers` - публичный метод добавления заголовков
 + `_encode_body` - кодирование тела ответа
 + `__call__` - магический метод, делает объект Response вызываемым
 + `json` - свойство класса для получения тела ответа в виде json

---

[Содержание](./index.md)

