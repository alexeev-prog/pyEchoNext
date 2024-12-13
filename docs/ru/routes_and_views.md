 # pyEchoNext / Создание маршрутов (routes&views)

---

Маршруты - основа веб приложения.

В pyEchoNext есть два метода создания маршрутов веб-страниц:

 + Django-like: создание наследника класса PageController, помещение его в датакласс URL и передача в виде аргумента urls в объект класса главного приложения EchoNext
 + Flask-like: создание функций с декоратором EchoNext.route_page.

Пример flask-like:

```python
import os
from pyechonext.app import ApplicationType, EchoNext
from pyechonext.config import Settings
from sqlsymphony_orm.datatypes.fields import IntegerField, RealField, TextField
from sqlsymphony_orm.models.session_models import SessionModel
from sqlsymphony_orm.models.session_models import SQLiteSession
from pyechonext.middleware import middlewares


settings = Settings(
  BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"
)
echonext = EchoNext(__name__, settings, middlewares, application_type=ApplicationType.HTML)
session = SQLiteSession("echonext.db")


class User(SessionModel):
  __tablename__ = "Users"

  id = IntegerField(primary_key=True)
  name = TextField(null=False)
  cash = RealField(null=False, default=0.0)

  def __repr__(self):
    return f"<User {self.pk}>"


@echonext.route_page("/")
def home(request, response):
  user = User(name="John", cash=100.0)
  session.add(user)
  session.commit()
  return "Hello from the HOME page"


@echonext.route_page("/users")
def about(request, response):
  users = session.get_all_by_model(User)

  return f"Users: {[f'{user.name}: {user.cash}$' for user in users]}"
```

Пример django-like и flask-like:

```python
import os

from pyechonext.app import ApplicationType, EchoNext
from pyechonext.config import Settings
from pyechonext.middleware import middlewares
from pyechonext.mvc.controllers import PageController
from pyechonext.urls import URL


class UsersPageController(PageController):
  def get(self, request, response, **kwargs):
    return "users get"

  def post(self, request, response, **kwargs):
    return "users post"


url_patterns = [URL(path="/users", controller=UsersPageController)]
settings = Settings(
  BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"
)
echonext = EchoNext(
  __name__,
  settings,
  middlewares,
  urls=url_patterns,
  application_type=ApplicationType.HTML,
)


@echonext.route_page("/book")
class BooksResource(PageController):
  def get(self, request, response, **kwargs):
    return f"Books Page: {request.GET}"

  def post(self, request, response, **kwargs):
    return "Endpoint to create a book"

```

Оба метода можно смешивать, но мы рекомендуем использовать только один в одном веб-приложении.

## PageController
PageController - "контроллеры", специальный класс для отображения страниц сайта. Вдохновлен стилем Django. Но в отличии от него, соответствуют паттерну MVC:

MVC - Model-View-Controller, архитектурный паттерн, который разделяет приложение на три логических компонента: модель, View (представление) и контроллер.

Основная идея паттерна MVC в том, что у каждого раздела кода есть своя цель. Часть кода содержит данные приложения, друга отвечает за то, каким видит его пользователь, последняя управлеяет его работой.

 + Код модели **Model** хранит данные и связанную с ними логику, а также закрепляет структуру приложения. То есть программист по шаблону будет определять основные компоненты приложения.
 + Код внешнего вида приложения, **View**, состоит из функций, которые отвечают за интерфейс и способы взаимодействия пользователя с ним. Представления создают на основе данных, собранных из модели.
 + Код контроллера, **Controller**, связывает модель и представление. Он получает на вход пользовательский ввод, интепретирует его и информирует о необходимых изменениях. Например, отправляет команды для обновления состояния, таких как сохранение документа.

```python

class BaseController(ABC):
  """
  Controls the data flow into a base object and updates the view whenever data changes.
  """

  @abstractmethod
  def get(self, request: Request, response: Response, *args, **kwargs):
    """
    Get method

    :param    request:        The request
    :type   request:        Request
    :param    response:       The response
    :type   response:       Response
    :param    args:         The arguments
    :type   args:         list
    :param    kwargs:         The keywords arguments
    :type   kwargs:         dictionary

    :raises   NotImplementedError:  abstract method
    """
    raise NotImplementedError()

  @abstractmethod
  def post(self, request: Request, response: Response, *args, **kwargs):
    """
    Post method

    :param    request:        The request
    :type   request:        Request
    :param    response:       The response
    :type   response:       Response
    :param    args:         The arguments
    :type   args:         list
    :param    kwargs:         The keywords arguments
    :type   kwargs:         dictionary

    :raises   NotImplementedError:  abstract method
    """
    raise NotImplementedError()


class PageController(BaseController):
  """
  Controls the data flow into a page object and updates the view whenever data changes.
  """

  def _create_model(
    self, request: Request, data: Union[Response, Any], app: "EchoNext"
  ) -> PageModel:
    """
    Creates a model.

    :param    request:  The request
    :type   request:  Request
    :param    data:   The data
    :type   data:   Union[Response, Any]
    :param    app:    The application
    :type   app:    EchoNext

    :returns: The page model.
    :rtype:   PageModel
    """
    model = PageModel(request)
    model.response = model.get_response(data, app)

    return model

  def get_rendered_view(
    self, request: Request, data: Union[Response, Any], app: "EchoNext"
  ) -> str:
    """
    Gets the rendered view.

    :param    request:  The request
    :type   request:  Request
    :param    data:   The data
    :type   data:   Union[Response, Any]
    :param    app:    The application
    :type   app:    EchoNext

    :returns: The rendered view.
    :rtype:   str
    """
    model = self._create_model(request, data, app)

    view = PageView()

    return view.render(model)

  def get(self, request: Request, response: Response, *args, **kwargs):
    """
    Get Method

    :param    request:     The request
    :type   request:     Request
    :param    response:    The response
    :type   response:    Response
    :param    args:      The arguments
    :type   args:      list
    :param    kwargs:      The keywords arguments
    :type   kwargs:      dictionary

    :raises   MethodNotAllow:  get method not allowed
    """
    raise MethodNotAllow("Method Not Allow: GET")

  def post(self, request: Request, response: Response, *args, **kwargs):
    """
    Post Method

    :param    request:     The request
    :type   request:     Request
    :param    response:    The response
    :type   response:    Response
    :param    args:      The arguments
    :type   args:      list
    :param    kwargs:      The keywords arguments
    :type   kwargs:      dictionary

    :raises   MethodNotAllow:  post method not allowed
    """
    raise MethodNotAllow("Method Not Allow: Post")

```

Для передачи их в приложение EchoNext требуется объединять Views в URL:

```python
@dataclass
class URL:
  """
  This dataclass describes an url.
  """

  path: str
  controller: Type[PageController]


url_patterns = [URL(url="/", view=<ВАШ КОНТРОЛЛЕР>)]
```

## Routes
Routes вдохновлены путем flask/fastapi:

```python
import os
from pyechonext.app import ApplicationType, EchoNext
from pyechonext.config import Settings
from pyechonext.middleware import middlewares
from pyechonext.mvc.controllers import PageController


settings = Settings(
  BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"
)
echonext = EchoNext(
  __name__, settings, middlewares, application_type=ApplicationType.HTML
)


@echonext.route_page("/")
def home(request, response):
  return "Hello from the HOME page"


@echonext.route_page("/book")
class BooksResource(PageController):
  def get(self, request, response, **kwargs):
    return f"GET Params: {request.GET}"

  def post(self, request, response, **kwargs):
    return f"POST Params: {request.POST}"
```

Вы можете также и маршрутизировать PageController без передачи их в параметры, а создавая класс с декоратором роутинга страницы.

---

[Содержание](./index.md)
