# pyEchoNext / создание веб-приложения

---

Создать приложение не является сложным в pyEchoNext. Благодаря модульности и универсальности можно настроить многие параметры и использовать разные методы создания маршрутов веб-приложения.

 > В скобках может быть указан нужный модуль для импортирования, т.е. где хранится данная абстракция. ex. EchoNext (pyechonext.app): from echonext.app import EchoNext

Основной является класс EchoNext (pyechonext.app):

```python
echonext = Echonext(app_name: str,
		settings: Settings,
		middlewaries: List[BaseMiddleware]
		urls: Optional[List[URL]],
		application_type: Optional[ApplicationType])
```

## Settings
Данный аргумент является экземпляром датакласса Settings (pyechonext.config).

```python
@dataclass
class Settings:
	"""
	This class describes settings.
	"""

	BASE_DIR: str
	TEMPLATES_DIR: str
	SECRET_KEY: str
	LOCALE: str = "DEFAULT"
	LOCALE_DIR: str = None
```

Создайте экземпляр:

```python
settings = Settings(
	BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates",
	SECRET_KEY='your-secret-key'
)
```

BASE_DIR - базовая директория файла приложения, TEMPLATES_DIR - директория html-шаблонов (для встроенного шаблонизатора или Jinja2).

Также, с версии 0.4.3 вы можете использовать специальный загрузчик настроек. На данный момент он позволяет загружать настройки с трех видов файлов:

 + env-файл (переменные окружения)
 + ini-файл
 + pymodule (модуль python)

Для его использования импортируйте:

```python
from pyechonext.config import SettingsLoader, SettingsConfigType
```

SettingsLoader - и есть загрузчик, а SettingsConfigType - enum-класс с видами конфиг-файлов.

SettingsLoader принимает следующие аргументы: `config_type: SettingsConfigType, filename: str`. Для получения настроек нужно вызвать метод `get_settings()`. Он возвращает объект датакласса Settings, его можно сразу передать в EchoNext-приложение.

SettingsConfigType содержит следующие значения:

```python
class SettingsConfigType(Enum):
	"""
	This class describes a settings configuration type.
	"""

	INI = 'ini'
	DOTENV = 'dotenv'
	PYMODULE = 'pymodule'
```

Примеры загрузки конфига:

### DOTENV

```python
config_loader = SettingsLoader(SettingsConfigType.DOTENV, 'example_env')
settings = config_loader.get_settings()
```

Файл example_env:

```env
PEN_BASE_DIR=.
PEN_TEMPLATES_DIR=templates
PEN_SECRET_KEY=secret-key
PEN_LOCALE=RU_RU
PEN_LOCALE_DIR=locales
```

### INI

```python
config_loader = SettingsLoader(SettingsConfigType.INI, 'example_ini.ini')
settings = config_loader.get_settings()
```

Файл example_ini.ini:

```ini
[Settings]
BASE_DIR=.
TEMPLATES_DIR=templates
SECRET_KEY=secret-key
LOCALE=DEFAULT
```

### PyModule

```python
config_loader = SettingsLoader(SettingsConfigType.PYMODULE, 'example_module.py')
settings = config_loader.get_settings()
```

Файл example_module.py:

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = 'templates'
SECRET_KEY = 'secret-key'
LOCALE = 'DEFAULT'
LOCALE_DIR = None
```

## Middlewares
Middlewares - "промежуточное ПО". Класс BaseMiddleware имеет следующий вид:

```python
class BaseMiddleware(ABC):
	"""
	This abstract class describes a base middleware.
	"""

	@abstractmethod
	def to_request(self, request: Request):
		"""
		To request method

		:param      request:  The request
		:type       request:  Request
		"""
		raise NotImplementedError

	@abstractmethod
	def to_response(self, response: Response):
		"""
		To response method

		:param      response:  The response
		:type       response:  Response
		"""
		raise NotImplementedError
```

Для создания своего Middleware вам нужно создать новый класс на основе этого класса и обязательно реализовать методы to_request и to_response. В pyEchoNext существует базовый Middleware для создания сессий:

```python
class SessionMiddleware(BaseMiddleware):
	"""
	This class describes a session (cookie) middleware.
	"""

	def to_request(self, request: Request):
		"""
		Set to request

		:param      request:  The request
		:type       request:  Request
		"""
		cookie = request.environ.get('HTTP_COOKIE', None)
		
		if not cookie:
			return

		session_id = parse_qs(cookie)['session_id'][0]
		request.extra['session_id'] = session_id

	def to_response(self, response: Response):
		"""
		Set to response

		:param      response:  The response
		:type       response:  Response
		"""
		if not response.request.session_id:
			response.add_headers([
				("Set-Cookie", f'session_id={uuid4()}'),
			])
```

Также в pyechonext.middleware есть базовый список `middlewares`, для передачи в аргументы EchoNext:

```python
middlewares = [
	SessionMiddleware
]
```

Таким образом вы можете импортирвать его и использовать или дополнить.

## URLS
По умолчанию `urls` равен пустому списку. urls содержит в себе экземпляры датакласса URL (pyechonext.urls):

```python
@dataclass
class URL:
	url: str
	view: Type[View]
```

View - это и есть абстракция маршрута сайта (django-like). Он обязательно должен иметь два метода: `get` и `post` (для ответа на get и post запросы). Эти методы должны возвращать:

 + Данные, контент страницы. Это может быть словарь или строка.

ИЛИ:

 + Объект класса Response (pyechonext.response)

View представляет собой объект класса View (pyechonext.views):

```python
class View(ABC):
	"""
	Page view
	"""

	@abstractmethod
	def get(self, request: Request, response: Response, *args, **kwargs) -> Union[Response, Any]:
		"""
		Get

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		args:	   The arguments
		:type		args:	   list
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary
		"""
		raise NotImplementedError

	@abstractmethod
	def post(self, request: Request, response: Response, *args, **kwargs) -> Union[Response, Any]:
		"""
		Post

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		args:	   The arguments
		:type		args:	   list
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary
		"""
		raise NotImplementedError
```

Для примера, в pyechonext.views есть IndexView, пример реализации View.

```python
class IndexView(View):
	def get(self, request: Request, response: Response, **kwargs) -> Union[Response, Any]:
		"""
		Get

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		args:	   The arguments
		:type		args:	   list
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary
		"""
		return "Hello World!"

	def post(self, request: Request, response: Response, **kwargs) -> Union[Response, Any]:
		"""
		Post

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		args:	   The arguments
		:type		args:	   list
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary
		"""
		return "Message has accepted!"
```

Эта реализация возвращает строку. Но также можно возвратить Response:

```python
class IndexView(View):
	def get(self, request: Request, response: Response, **kwargs) -> Union[Response, Any]:
		"""
		Get

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		args:	   The arguments
		:type		args:	   list
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary
		"""
		return Response(request, body='Hello World!')

	def post(self, request: Request, response: Response, **kwargs) -> Union[Response, Any]:
		"""
		Post

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		args:	   The arguments
		:type		args:	   list
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary
		"""
		return Response(request, body='Message has accepted!')
```

Можно комбинировать эти два способа. По их использованию есть следующие рекомендации:

1. Если метод только возвращает уже подготовленные данные, то не следует возвращать Response, возвращайте данные.
2. Если метод работает с переданным ему response, то возвращайте данные или сам переданный в аргументах response.
3. В остальных случаях можно создавать Response и возвращать его, а не данные.
4. В get и post методе стоит использовать только один способ, не стоит их смешивать. Но если без этого не обойтись, то эту рекомендацию можно нарушить.

Эти рекомендации могут нарушаться по желанию разработчика.

Также вместо возвращения результата можно вызывать исключения WebError: URLNotFound и MethodNotAllow. В таком случае приложение не прекратит свою работу, а будет выводить ошибку на стороне веб-страницы. В случае же другого исключения приложение прекратит свою работу.

В pyechonext.urls также существует базовый список для передачи его в аргументы EchoNext:

```python
url_patterns = [URL(url="/", view=IndexView)]
```

IndexView здесь - это встроенный View, который вы могли увидеть выше.

## application_type
application_type - тип приложения. Аргумент принимает enum-класс ApplicationType:

```python
class ApplicationType(Enum):
	"""
	This enum class describes an application type.
	"""

	JSON = "application/json"
	HTML = "text/html"
	PLAINTEXT = "text/plain"
```

Пока поддерживается: ApplicationType.JSON, ApplicationType.HTML, ApplicationType.PLAINTEXT.

По умолчанию равен ApplicationType.JSON.

---

[Содержание](./index.md)
