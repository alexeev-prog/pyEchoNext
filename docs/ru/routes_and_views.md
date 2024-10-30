# pyEchoNext / Создание маршрутов (routes&views)

Маршруты - основа веб приложения.

В pyEchoNext есть два метода создания маршрутов веб-страниц:

 + Django-like: создание наследника класса View, помещение его в датакласс URL и передача в виде аргумента urls в объект класса главного приложения EchoNext
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
from pyechonext.utils.exceptions import MethodNotAllow
from pyechonext.app import ApplicationType, EchoNext
from pyechonext.views import View
from pyechonext.urls import URL, IndexView
from pyechonext.config import Settings
from pyechonext.template_engine.jinja import render_template
from pyechonext.middleware import middlewares


class UsersView(View):
  def get(self, request, response, **kwargs):
    return render_template(
      request, "index.html", user_name="User", session_id=request.session_id, friends=["Bob", "Anna", "John"]
    )

  def post(self, request, response, **kwargs):
    raise MethodNotAllow(f'Request {request.path}: method not allow')


url_patterns = [URL(url="/", view=IndexView), URL(url="/users", view=UsersView)]
settings = Settings(
  BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"
)
echonext = EchoNext(
  __name__, settings, middlewares, urls=url_patterns, application_type=ApplicationType.HTML
)


@echonext.route_page("/book")
class BooksResource(View):
  def get(self, request, response, **kwargs):
    return f"GET Params: {request.GET}"

  def post(self, request, response, **kwargs):
    return f"POST Params: {request.POST}"
```

Оба метода можно смешивать, но мы рекомендуем использовать только один в одном веб-приложении.

---

[Содержание](./index.md)
