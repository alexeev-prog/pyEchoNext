.. pyEchoNext documentation master file, created by
   sphinx-quickstart on Fri Apr 18 00:12:47 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyEchoNext documentation
========================


.. toctree::
   :maxdepth: 2
   :caption: Article Docs:
   
   webframework_design
   webapp_creation
   routes_and_views
   requests_responses
   security
   mvc
   permissions
   

------------------

.. toctree::
   :maxdepth: 2
   :caption: Source code docs:
   
   pyechonext
   pyechonext.app
   pyechonext.middleware
   pyechonext.permissions
   pyechonext.request
   pyechonext.response
   pyechonext.static
   pyechonext.urls
   pyechonext.cache
   pyechonext.config
   pyechonext.apidoc_ui
   pyechonext.auth
   pyechonext.docsgen
   pyechonext.logging
   pyechonext.template_engine
   pyechonext.utils

------------------

🌟 **EchoNext: The Future of Web** 🚀
=====================================

.. container::

   .. raw:: html

      <p align="center">

   EchoNext is a lightweight, fast and scalable web framework for Python
   Explore the docs » Why Choose pyEchoNext · Key Features · Getting
   Started · Basic Usage · Specification · Documentation · License

   .. raw:: html

      </p>

.. raw:: html

   <p align="center">

.. raw:: html

   </p>

.. raw:: html

   <p align="center">

.. raw:: html

   </p>

..

   EchoNext is a lightweight, fast and scalable web framework for Python

   [!CAUTION] At the moment, EchoNext is under active development, many
   things may not work, and this version is not recommended for use (all
   at your own risk)

Welcome to **EchoNext**, where innovation meets simplicity! Are you
tired of the sluggishness of traditional web frameworks? Want a solution
that keeps pace with your ambitious apps? Look no further. EchoNext is
your agile companion in the world of web development!

   [!NOTE] Versions below 0.7.14a are not recommended for use with
   gunicorn <23.0 due to the fact that they used an older version of
   gunicorn (<23.0), which was
   `vulnerable <https://deps.dev/advisory/osv/GHSA-hc5x-x2vx-497g>`__.

.. raw:: html

   <p align="center">

.. raw:: html

   </p>

**Imagine** a lightweight framework that empowers you to create modern
web applications with lightning speed and flexibility. With EchoNext,
you’re not just coding; you’re building a masterpiece!

   Last stable version: 0.7.15 alpha

..

   Next Big Update: ASYNC & unicorn support

Check Other My Projects
-----------------------

-  `SQLSymphony <https://github.com/alexeev-prog/SQLSymphony>`__ -
   simple and fast ORM in sqlite (and you can add other DBMS)
-  `Burn-Build <https://github.com/alexeev-prog/burn-build>`__ - simple
   and fast build system written in python for C/C++ and other projects.
   With multiprocessing, project creation and caches!
-  `OptiArch <https://github.com/alexeev-prog/optiarch>`__ - shell
   script for fast optimization of Arch Linux
-  `libnumerixpp <https://github.com/alexeev-prog/libnumerixpp>`__ - a
   Powerful C++ Library for High-Performance Numerical Computing
-  `pycolor-palette <https://github.com/alexeev-prog/pycolor-palette>`__
   - display beautiful log messages, logging, debugging.
-  `shegang <https://github.com/alexeev-prog/shegang>`__ - powerful
   command interpreter (shell) for linux written in C

🤔 Why Choose pyEchoNext?
-------------------------

-  **🔥 Featherweight Performance**: No bloat, just speed! Our framework
   is designed to optimize performance, making it a breeze to create and
   scale your applications without the overhead.

-  **💼 Unmatched Scalability**: Handle thousands of connections
   effortlessly! Echonext is built for performance in high-demand
   environments, making it the perfect choice for startups or enterprise
   applications.

-  **🔧 Customizable Architecture**: Tailor your framework to suit your
   unique needs. Whether it’s middleware, routing, or authentication,
   make it yours with minimal effort!

-  **🌍 Cross-Platform Compatibility**: Echonext works beautifully on
   any OS. Whether you’re developing on Windows, macOS, or Linux, you’re
   covered!

-  **💡 User-Friendly Design**: Our intuitive API and comprehensive
   documentation make it easy for beginners and pros alike. Dive in and
   start coding right away!

-  **📦 Plug-and-Play Components**: Easily integrate with third-party
   libraries to enhance your application. Don’t reinvent the
   wheel—leverage existing solutions!

-  **🔒 Built-in Authentication**: Simplify your user authentication
   process with our built-in, easy-to-implement features.

-  **📊 Automatic API Documentation**: Create RESTful endpoints that are
   not just powerful but also well-documented, saving you time and
   effort.

.. raw:: html

   <p align="right">



.. raw:: html

   </p>

📚 Key Features
---------------

-  Intuitive API: Pythonic, object-oriented interface for interacting
   with routes and views.
-  Performance Optimization: Lazy loading, eager loading, and other
   techniques for efficient web queries.
-  Comprehensive Documentation: Detailed usage examples and API
   reference to help you get started.
-  Modular Design: Clean, maintainable codebase that follows best
   software engineering practices.
-  Extensive Test Coverage: Robust test suite to ensure the library’s
   reliability and stability.

.. raw:: html

   <p align="right">



.. raw:: html

   </p>

⚙️ Functionality
----------------

-  i18n/l10n localization with
   `hermes-langlib <https://github.com/alexeev-prog/hermes_langlib>`__.
-  basic project documentation generator
-  request/response
-  middlewares (with basic session cookie middleware)
-  views and routes
-  settings and config loader
-  built-in template engine and Jinja2
-  basic security and hashing
-  static files management
-  cache response bodies
-  performance
-  slugger
-  permissions

.. raw:: html

   <p align="right">



.. raw:: html

   </p>

🚀 Getting Started
------------------

pyEchoNext is available on
`PyPI <https://pypi.org/project/pyechonext>`__. Simply install the
package into your project environment with PIP:

.. code:: bash

   pip install pyechonext

Once installed, you can start using the library in your Python projects.
Check out the
`documentation <https://alexeev-prog.github.io/pyEchoNext>`__ for
detailed usage examples and API reference.

.. raw:: html

   <p align="right">



.. raw:: html

   </p>

⚙️ Dependency Injection
-----------------------

pyEchoNext is universal, and you are free to use any
Dependency-Injection framework. But we recommend using the specially
developed `echonextdi <https://github.com/alexeev-prog/echonext_di>`__.
It is simple and fast to use.

Install:

.. code:: bash

   pip install echonextdi

Example code:

.. code:: python

   from echonextdi.containers.container import Container
   from echonextdi.depends import Depends
   from echonextdi.providers.callable_provider import CallableProvider


   def sqrt(a: int, b: int = 2):
       return a**b


   class SQRT_Dependency:
       def __init__(self, sqrt):
           self.sqrt = sqrt


   container = Container()
   container.register("sqrt", CallableProvider(sqrt))


   def calculate(number: int, depend: Depends = Depends(container, SQRT_Dependency)):
       print(f"{number} ^2 = {depend().sqrt(2)}")


   calculate(4) # Output: 16

💻 Usage Examples
-----------------

You can view examples at `examples directory <./examples>`__.

i18n with hermes-langlib
~~~~~~~~~~~~~~~~~~~~~~~~

Hermes LangLib - a fast and light python library for translating,
localizing and internationalizing your applications. The library is
aimed at high speed and stability; it can be used in highly loaded
projects.

Directory tree:

::

   ├── example.toml
   └── locales
       └── default.json

Example config-file ``example.toml``:

.. code:: toml

   locale_directory="locales"
   default_locale_file="default.json"
   default_language="RU_RU"
   translator="google"

Example locale file ``locales/default.json``:

.. code:: json

   {
     "locales": {
       "RU": ["RU_RU"],
       "EN": ["EN_EN", "EN_US"]
     },
     "RU": {
       "RU_RU": {
         "title": "Библиотека для интернационализации",
         "description": "Библиотека, которая позволит переводить ваши приложения",
         "mails_message": {
           "plural": "count",
           "^0$": "У вас нет ни одного письма",
           "11": "У вас есть {count} писем",
           "1$|1$": "У вас есть {count} письмо",
           "^(2|3|4)$|(2|3|4)$": "У вас есть {count} письма",
           "other": "У вас есть {count} писем"
         }
       }
     },
     "EN": {
       "EN_EN": {
         "title": "Library for internationalization",
         "description": "A library that will allow you to translate your applications",
         "mails_message": {
           "plural": "count",
           "^0$": "You do not have any mail.",
           "^1$": "You have a new mail.",
           "other": "You have {count} new mails."
         }
       },
       "EN_US": {
         "title": "Library for internationalization",
         "description": "A library that will allow you to translate your applications",
         "mails_message": {
           "plural": "count",
           "^0$": "You do not have any mail.",
           "^1$": "You have a new mail.",
           "other": "You have {count} new mails."
         }
       }
     }
   }

Example usage:

.. code:: python

   from hermes_langlib.locales import LocaleManager
   from hermes_langlib.storage import load_config

   config = load_config('example.toml')

   locale_manager = LocaleManager(config)
   print(locale_manager.get('title - {version}', 'default', 'RU_RU', version="0.1.0"))
   print(locale_manager.get('title - {version}', 'default', 'RU', version="0.1.0"))
   print(locale_manager.get('mails_message.', 'default', 'RU_RU', count=0))
   print(locale_manager.get('mails_message', 'default', 'RU_RU', count=1))
   print(locale_manager.get('mails_message', 'default', 'RU_RU', count=11))
   print(locale_manager.get('mails_message', 'default', 'RU_RU', count=2))
   print(locale_manager.get('mails_message', 'default', 'RU_RU', count=22))
   print(locale_manager.get('mails_message', 'default', 'RU_RU', count=46))
   print(locale_manager.get('mails_message', 'default', 'RU_RU', count=100000001))
   print(locale_manager.translate("You have only three mails", "en", 'ru'))
   print(locale_manager.translate("У вас всего три письма", "ru", 'en'))

You can read `Hermes-Langlib Specification at this
link <https://github.com/alexeev-prog/hermes_langlib/tree/main?tab=readme-ov-file#-specifications>`__.

.. raw:: html

   <p align="right">



.. raw:: html

   </p>

Basic With Depends Injection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   import os

   from pyechonext.app import ApplicationType, EchoNext
   from pyechonext.config import Settings
   from pyechonext.middleware import middlewares
   from pyechonext.mvc.controllers import PageController
   from pyechonext.urls import URL

   from echonextdi.containers.container import Container
   from echonextdi.depends import Depends
   from echonextdi.providers.callable_provider import CallableProvider


   class IndexController(PageController):
       def get(self, request, response, **kwargs):
           return "Hello"

       def post(self, request, response, **kwargs):
           return "Hello"


   def say_hello(name: str, phrase: str = 'Hello'):
       return f'{phrase} {name}'


   class Hello_Dependency:
       def __init__(self, say_hello):
           self.say_hello = say_hello


   container = Container()
   container.register("say_hello", CallableProvider(say_hello))

   url_patterns = [URL(path="/", controller=IndexController)]
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


   @echonext.route_page("/hello/{name}")
   def hello(request, response, name: str = "World", depend: Depends = Depends(container, Hello_Dependency)):
       response.body = depend().say_hello(name)

Performance caching
~~~~~~~~~~~~~~~~~~~

.. code:: python

   import random
   from pyechonext.utils.performance import InMemoryPerformanceCache, SingletonPerformanceCache, performance_cached

   memorycache = InMemoryPerformanceCache
   perf = SingletonPerformanceCache(memorycache)


   @performance_cached(perf)
   def example_function(a: int = 10 ** 6):
       inside_circle = 0

       for _ in range(a):
           x = random.uniform(-1, 1)
           y = random.uniform(-1, 1)
           if x ** 2 + y ** 2 <= 1:
               inside_circle += 1

       return (inside_circle / a) * 4


   if __name__ == '__main__':
       print('start')
       print(f'{example_function()} - Caching')
       print(f'{example_function()} - Cached')
       print(f'{example_function(10 ** 7)} - Caching new')

Permissions
~~~~~~~~~~~

.. code:: python

   from pyechonext.permissions import (
       Permission,
       Role,
       Resource,
       AccessControlRule,
       Policy,
       AgeRestrictionsABP,
       User,
       DefaultPermissionChecker,
       UserController,
   )

   view_users_perm = Permission("view_users")
   edit_users_perm = Permission("edit_users")

   admin_role = Role("admin")
   admin_role.add_permission(view_users_perm)
   admin_role.add_permission(edit_users_perm)

   user_role = Role("user")
   user_role.add_permission(view_users_perm)

   user_resource = Resource("UserResource")

   policy = Policy()
   policy.add_rule(AccessControlRule(admin_role, view_users_perm, user_resource, True))
   policy.add_rule(AccessControlRule(admin_role, edit_users_perm, user_resource, True))
   policy.add_rule(AccessControlRule(user_role, view_users_perm, user_resource, True))
   policy.add_rule(AccessControlRule(user_role, edit_users_perm, user_resource, False))

   age_policy = AgeRestrictionsABP(conditions={"age": 18}, rules=policy.rules)
   age_policy.add_rule(AccessControlRule(user_role, view_users_perm, user_resource, True))

   admin_user = User("admin", attributes={"age": 30})
   admin_user.add_role(admin_role)

   young_user = User("john_doe", attributes={"age": 17})
   young_user.add_role(user_role)

   permission_checker = DefaultPermissionChecker(policy)
   user_controller = UserController(permission_checker)


   def main():
       assert user_controller.view_users(admin_user, user_resource) == (
           "200 OK",
           "User edit form",
       )
       assert user_controller.edit_users(admin_user, user_resource) == (
           "200 OK",
           "User edit form",
       )
       assert user_controller.edit_users(young_user, user_resource) == (
           "403 Forbidden",
           "You do not have permission to edit users.",
       )

       assert age_policy.evaluate(young_user, user_resource, view_users_perm) == False
       assert age_policy.evaluate(admin_user, user_resource, view_users_perm) == True


   if __name__ == "__main__":
       main()

.. raw:: html

   <p align="right">



.. raw:: html

   </p>

🔧 Specifications
-----------------

Security
~~~~~~~~

A security module created for hash functions and crypto-algorithms.

Crypts
^^^^^^

Simple crypto-algorithms.

PSPCAlgorithm
'''''''''''''

Point Simple Password Crypt Algorithm.

::

   Base: AngryPassword
   Crypted: 00778.87999.74379.363401.558001.558001.96058.06107.711601.87999.13309.07469.50075
   Decrypted: AngryPassword

   Base: S0mesd7623tds@&6^@_
   Crypted: 51338.82165.83428.85374.62333.82165.558001.00778.237101.72744.05834.85374.53284.00778.558001.77588.39559.69024.19727
   Decrypted: S0mesd7623tds@&6^@_

   Base: PassWord
   Crypted: 00778.87999.74379.99267.558001.558001.96058.06107
   Decrypted: PassWord

   Base: Pass
   Crypted: 558001.558001.96058.06107
   Decrypted: Pass

Example:

.. code:: python

   from pyechonext.security.crypts import PSPCAlgorithm


   pspc = PSPCAlgorithm()

   passwords = ['AngryPassword', 'S0mesd7623tds@&6^@_', 'PassWord', 'Pass']

   for password in passwords:
       print('Base:', password)
       print('Crypted:', pspc.crypt(password))
       print('Decrypted:', pspc.decrypt(pspc.crypt(password)))
       print()

Hashing
^^^^^^^

-  Module: ``pyechonext.security.hashing``

HashAlgorithm
'''''''''''''

Enum class with available hashing algorithms

.. code:: python

   class HashAlgorithm(Enum):
       """
       This class describes a hash algorithms.
       """

       SHA256 = auto()
       SHA512 = auto()
       MD5 = auto()
       BLAKE2B = auto()
       BLAKE2S = auto()

PlainHasher
'''''''''''

A simple class for hashing text. Has no ‘salting’.

.. code:: python

   hasher = PlainHasher(HashAlgorithm.BLAKE2S)
   old_hash = hasher.hash("TEXT")
   new_hash = hasher.hash("TEXT")

   if hasher.verify("TEXT", new_hash): # true
       print('Yes!')

   if hasher.verify("TEXT2", old_hash): # false
       print('Yes!')

   # Output: one "Yes!"

SaltedHasher
''''''''''''

A simple class for hashing text. Has hash salt.

.. code:: python

   hasher = SaltedHasher(HashAlgorithm.BLAKE2S, salt='bob')
   old_hash = hasher.hash("TEXT")
   new_hash = hasher.hash("TEXT")

   if hasher.verify("TEXT", new_hash): # true
       print('Yes!')

   if hasher.verify("TEXT2", old_hash): # false
       print('Yes!')

   # Output: one "Yes!"

View
~~~~

View is an abstract class, with abstract get and post methods (all
descendants must create these methods).

.. code:: python

   class View(ABC):
       """
       Page view
       """

       @abstractmethod
       def get(self, request: Request, response: Response, *args, **kwargs):
           """
           Get

           :param      request:   The request
           :type       request:   Request
           :param      response:  The response
           :type       response:  Response
           :param      args:      The arguments
           :type       args:      list
           :param      kwargs:    The keywords arguments
           :type       kwargs:    dictionary
           """
           raise NotImplementedError

       @abstractmethod
       def post(self, request: Request, response: Response, *args, **kwargs):
           """
           Post

           :param      request:   The request
           :type       request:   Request
           :param      response:  The response
           :type       response:  Response
           :param      args:      The arguments
           :type       args:      list
           :param      kwargs:    The keywords arguments
           :type       kwargs:    dictionary
           """
           raise NotImplementedError

Example of view:

.. code:: python

   class IndexView(View):
       def get(self, request: Request, response: Response, **kwargs):
           """
           Get

           :param      request:   The request
           :type       request:   Request
           :param      response:  The response
           :type       response:  Response
           :param      args:      The arguments
           :type       args:      list
           :param      kwargs:    The keywords arguments
           :type       kwargs:    dictionary
           """
           return "Hello World!"

       def post(self, request: Request, response: Response, **kwargs):
           """
           Post

           :param      request:   The request
           :type       request:   Request
           :param      response:  The response
           :type       response:  Response
           :param      args:      The arguments
           :type       args:      list
           :param      kwargs:    The keywords arguments
           :type       kwargs:    dictionary
           """
           return "Message has accepted!"

Or you can return response:

.. code:: python

   class IndexView(View):
       def get(self, request: Request, response: Response, **kwargs):
           """
           Get

           :param      request:   The request
           :type       request:   Request
           :param      response:  The response
           :type       response:  Response
           :param      args:      The arguments
           :type       args:      list
           :param      kwargs:    The keywords arguments
           :type       kwargs:    dictionary
           """
           return Response(request, body="Hello World!")

       def post(self, request: Request, response: Response, **kwargs):
           """
           Post

           :param      request:   The request
           :type       request:   Request
           :param      response:  The response
           :type       response:  Response
           :param      args:      The arguments
           :type       args:      list
           :param      kwargs:    The keywords arguments
           :type       kwargs:    dictionary
           """
           return Response(request, body="Message has accepted!")

Tests coverage
--------------

To test the web framework, PyTest with the pytest-cov plugin is used.
You can look at the tests in `tests directory <./tests>`__

Documentation 🌍
----------------

The main documentation is
`here <https://alexeev-prog.github.io/pyEchoNext/>`__.

💬 Support
----------

If you encounter any issues or have questions about pyEchoNext, please:

-  Check the
   `documentation <https://alexeev-prog.github.io/pyEchoNext>`__ for
   answers
-  Open an `issue on
   GitHub <https://github.com/alexeev-prog/pyEchoNext/issues/new>`__
-  Reach out to the project maintainers via the `mailing
   list <mailto:alexeev.dev@mail.ru>`__

.. raw:: html

   <p align="right">



.. raw:: html

   </p>

🤝 Contributing
---------------

We welcome contributions from the community! If you’d like to help
improve pyEchoNext, please check out the `contributing
guidelines <https://github.com/alexeev-prog/pyEchoNext/blob/main/CONTRIBUTING.md>`__
to get started.

.. raw:: html

   <p align="right">



.. raw:: html

   </p>

👥 Join the Community!
----------------------

If you find Echonext valuable and want to support the project:

-  Star on GitHub ⭐
-  Share it with friends and colleagues!
-  Donate via cryptocurrency 🙌

Connect with fellow Echonext users: `Join our Telegram
Chat <https://t.me/pyEchoNext_Forum>`__

🔮 Roadmap
----------

Our future goals for pyEchoNext include:

-  📚 Improve middlewares
-  🚀 Add async support
-  ✅ Improve logging
-  🌍 Add authentication, JWT tokens
-  💻 Depedency Injection
-  🌐 More stability and scalablity

.. raw:: html

   <p align="right">



.. raw:: html

   </p>

🌟 Get Started Today!
---------------------

Unlock your potential as a developer with Echonext. Don’t just build
applications—craft experiences that resonate with your users! The
possibilities are limitless when you harness the power of Echonext.

**Happy Coding!** 💻✨

This README is designed to grab attention from the very first lines. It
emphasizes the framework’s strengths and makes a compelling case for why
developers should choose Echonext for their projects. Feel free to
adjust any specific links or images to fit your project!

License
-------

Distributed under the GNU LGPL 2.1 License. See
`LICENSE <https://github.com/alexeev-prog/pyEchoNext/blob/main/LICENSE>`__
for more information.

.. raw:: html

   <p align="right">



.. raw:: html

   </p>

--------------

EchoNext is a lightweight, fast and scalable web framework for Python
Copyright (C) 2024 Alexeev Bronislav (C) 2024

This library is free software; you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or (at
your option) any later version.

This library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this library; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA