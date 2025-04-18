pyEchoNext / creating a web application
=======================================

--------------

Creating an application is not difficult in pyEchoNext. Thanks to its
modularity and versatility, you can configure many settings and use
different methods for creating web application routes.

   The required module to import can be indicated in parentheses,
   i.e. where this abstraction is stored. ex. EchoNext (pyechonext.app):
   from echonext.app import EchoNext

The main one is the EchoNext class (pyechonext.app):

.. code:: python

   echonext = Echonext(app_name: str,
   settings: Settings,
   middlewaries: List[BaseMiddleware]
   urls: Optional[List[URL]],
   application_type: Optional[ApplicationType])

Settings
--------

This argument is an instance of the Settings dataclass
(pyechonext.config).

.. code:: python

   @dataclass
   class Settings:
      """
      This class describes settings.
      """

      BASE_DIR: str
      TEMPLATES_DIR: str
      SECRET_KEY: str
      VERSION: str = '1.0.0'
      DESCRIPTION: str = 'Echonext webapp'
      LOCALE: str = "DEFAULT"
      LOCALE_DIR: str = None

Create an instance:

.. code:: python

   settings = Settings(
      BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates",
      SECRET_KEY='your-secret-key'
   )

BASE_DIR - base directory of the application file, TEMPLATES_DIR -
directory of html templates (for the built-in template engine or
Jinja2).

Also, from version 0.4.3 you can use a special settings loader. At the
moment, it allows you to load settings from three types of files:

-  env file (environment variables)
-  ini file
-  pymodule (python module)

To use it, import:

.. code:: python

   from pyechonext.config import SettingsLoader, SettingsConfigType

SettingsLoader is the loader, and SettingsConfigType is an enum class
with types of config files.

SettingsLoader accepts the following arguments:
``config_type: SettingsConfigType, filename: str``. To get settings you
need to call the ``get_settings()`` method. It returns an object of the
Settings data class, which can be immediately passed to the EchoNext
application.

SettingsConfigType contains the following values:

.. code:: python

   class SettingsConfigType(Enum):
      """
      This class describes a settings configuration type.
      """

      THIS = 'this'
      DOTENV = 'dotenv'
      PYMODULE = 'pymodule'

Examples of config loading:

DOTENV
~~~~~~

.. code:: python

   config_loader = SettingsLoader(SettingsConfigType.DOTENV, 'example_env')
   settings = config_loader.get_settings()

example_env file:

.. code:: env

   PEN_BASE_DIR=.
   PEN_TEMPLATES_DIR=templates
   PEN_SECRET_KEY=secret-key
   PEN_LOCALE=RU_RU
   PEN_LOCALE_DIR=local
   PEN_VERSION=1.0.0
   PEN_DESCRIPTION=Example

THIS
~~~~

.. code:: python

   config_loader = SettingsLoader(SettingsConfigType.INI, 'example_ini.ini')
   settings = config_loader.get_settings()

File example_ini.ini:

.. code:: this

   [Settings]
   BASE_DIR=.
   TEMPLATES_DIR=templates
   SECRET_KEY=secret-key
   LOCALE=DEFAULT
   VERSION=1.0.0
   DESCRIPTION=Example

PyModule
~~~~~~~~

.. code:: python

   config_loader = SettingsLoader(SettingsConfigType.PYMODULE, 'example_module.py')
   settings = config_loader.get_settings()

Example_module.py file:

.. code:: python

   import os

   BASE_DIR = os.path.dirname(os.path.abspath(__file__))
   TEMPLATES_DIR = 'templates'
   SECRET_KEY = 'secret-key'
   VERSION = '1.0.0'
   DESCRIPTION = 'Echonext webapp'
   LOCALE = 'DEFAULT'
   LOCALE_DIR = None

Middlewares
-----------

Middlewares - “middleware”. The BaseMiddleware class looks like this:

.. code:: python

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

To create your own Middleware, you need to create a new class based on
this class and be sure to implement the to_request and to_response
methods. pyEchoNext has a basic Middleware for creating sessions:

.. code:: python

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

There is also a basic list of ``middlewares`` in pyechonext.middleware
to pass as arguments to EchoNext:

.. code:: python

   middlewares = [
      SessionMiddleware
   ]

This way you can import it and use or add to it.

URLS
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

We use MVC (Model-View-Controller) model. To understand this, read :ref:`mvc`.

There is also a base list in pyechonext.urls to pass as arguments to
EchoNext:

.. code:: python

   url_patterns = [URL(url="/", view=IndexView)]

The IndexView here is the built-in View that you could see above.

application_type
----------------

application_type - application type. The argument takes an
ApplicationType enum class:

.. code:: python

   class ApplicationType(Enum):
      """
      This enum class describes an application type.
      """

      JSON = "application/json"
      HTML = "text/html"
      PLAINTEXT = "text/plain"

Currently supported: ApplicationType.JSON, ApplicationType.HTML,
ApplicationType.PLAINTEXT.

Defaults to ApplicationType.JSON.

--------------
