# pyEchoNext / создание веб-приложения
Создать приложение не является сложным в pyEchoNext. Благодаря модульности и универсальности можно настроить многие параметры и использовать разные методы создания маршрутов веб-приложения.

 > В скобках может быть указан нужный модуль для импортирования, т.е. где хранится данная абстракция. ex. EchoNext (pyechonext.app): from echonext.app import EchoNext

Основной является класс EchoNext (pyechonext.app):

```python
echonext = Echonext(app_name: str,
		settings: Settings,
		urls: Optional[List[URL]],
		application_type: Optional[ApplicationType])
```

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
		return Response(body='Hello World!')

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
		return Response(body='Message has accepted!')
```

Можно комбинировать эти два способа. По их использованию есть следующие рекомендации:

1. Если метод только возвращает уже подготовленные данные, то не следует возвращать Response, возвращайте данные.
2. Если метод работает с переданным ему response, то возвращайте данные или сам переданный в аргументах response.
3. В остальных случаях можно создавать Response и возвращать его, а не данные.
4. В get и post методе стоит использовать только один способ, не стоит их смешивать. Но если без этого не обойтись, то эту рекомендацию можно нарушить.

Эти рекомендации могут нарушаться по желанию разработчика.

Также вместо возвращения результата можно вызывать исключения WebError: URLNotFound и MethodNotAllow. В таком случае приложение не прекратит свою работу, а будет выводить ошибку на стороне веб-страницы. В случае же другого исключения приложение прекратит свою работу.

## Settings
Данный аргумент является экземпляром датакласса Settings (pyechonext.config)

---

[Содержание](./index.md)
