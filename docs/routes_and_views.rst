pyEchoNext / Creating routes (routes&views)
===========================================

--------------

Routes are the basis of a web application.

pyEchoNext has two methods for creating web page routes:

-  Django-like: creating a descendant of the View class, placing it in a
   URL dataclass and passing it as a urls argument to the EchoNext main
   application class object
-  Flask-like: creating functions with the EchoNext.route_page
   decorator.

Flask-like example:

.. code:: python

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

Example django-like and flask-like:

.. code:: python

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

Both methods can be mixed, but we recommend using only one per web
application.

Views
-----

Views - “views”, a special class for displaying site pages. Inspired by
Django style.

.. code:: python

   class View(ABC):
   """
   Page view
   """

   @abstractmethod
   def get(
   self, request: Request, response: Response, *args, **kwargs
   ) -> Union[Response, Any]:
   """
   Get

   :param    request:   The request
   :type   request:   Request
   :param    response:  The response
   :type   response:  Response
   :param    args:    The arguments
   :type   args:    list
   :param    kwargs:    The keywords arguments
   :type   kwargs:    dictionary
   """
   raise NotImplementedError

   @abstractmethod
   def post(
   self, request: Request, response: Response, *args, **kwargs
   ) -> Union[Response, Any]:
   """
   Post

   :param    request:   The request
   :type   request:   Request
   :param    response:  The response
   :type   response:  Response
   :param    args:    The arguments
   :type   args:    list
   :param    kwargs:    The keywords arguments
   :type   kwargs:    dictionary
   """
   raise NotImplementedError

To pass them to the EchoNext application, you need to combine Views into
a URL:

.. code:: python

   @dataclass
   class URL:
   """
   This dataclass describes an url.
   """

   url: str
   view: Type[View]


   url_patterns = [URL(url="/", view=<ВАШ View>)]

Example:

.. code:: python

   class IndexView(View):
   def get(
   self, request: Request, response: Response, **kwargs
   ) -> Union[Response, Any]:
   """
   Get

   :param    request:   The request
   :type   request:   Request
   :param    response:  The response
   :type   response:  Response
   :param    args:    The arguments
   :type   args:    list
   :param    kwargs:    The keywords arguments
   :type   kwargs:    dictionary
   """
   return "Hello World!"

   def post(
   self, request: Request, response: Response, **kwargs
   ) -> Union[Response, Any]:
   """
   Post

   :param    request:   The request
   :type   request:   Request
   :param    response:  The response
   :type   response:  Response
   :param    args:    The arguments
   :type   args:    list
   :param    kwargs:    The keywords arguments
   :type   kwargs:    dictionary
   """
   return "Message has accepted!"


   url_patterns = [URL(url="/", view=IndexView)]

Routes
------

Routes inspired by flask/fastapi path:

.. code:: python

   import os
   from pyechonext.app import ApplicationType, EchoNext
   from pyechonext.config import Settings
   from pyechonext.middleware import middlewares


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
   class BooksResource(View):
      def get(self, request, response, **kwargs):
         return f"GET Params: {request.GET}"

      def post(self, request, response, **kwargs):
         return f"POST Params: {request.POST}"

You can also route Views without passing them to parameters, but by
creating a class with a page routing decorator.

--------------
