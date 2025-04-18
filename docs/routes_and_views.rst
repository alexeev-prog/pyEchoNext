Creating routes (routes&views)
===========================================

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


URLs
----

By default, ``urls`` is an empty list. urls contains instances of the
URL dataclass (pyechonext.urls):

.. code:: python

   @dataclass
   class URL:
      path: str
	   controller: Type[PageController]
	   summary: Optional[str] = None

Controller is an abstraction of the site route (django-like). It must have two
methods: ``get`` and ``post`` (to respond to get and post requests).
These methods should return:

-  Data, page content. This can be a dictionary or a string.

OR:

-  Response class object (pyechonext.response)

You can combine these two methods. There are the following
recommendations for their use:

1. If the method only returns already prepared data, then you should not
   return Response, return data.
2. If the method works with the response passed to it, then return the
   data or the response itself passed in the arguments.
3. In other cases, you can create a Response and return it, not data.
4. In the get and post methods, you should use only one method, you
   should not mix them. But if you cannot do without it, then this
   recommendation can be violated.

These recommendations may be violated at the request of the developer.

You can also throw WebError exceptions instead of returning a result:
URLNotFound and MethodNotAllow. In this case, the application will not
stop working, but will display an error on the web page side. If another
exception occurs, the application will stop working.

We use MVC (Model-View-Controller) model. To understand this, read :doc:`MVC Docs </mvc>`.

There is also a base list in pyechonext.urls to pass as arguments to
EchoNext:

.. code:: python

   url_patterns = [URL(url="/", controller=MyController, summary="Page")]

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
