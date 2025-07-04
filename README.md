# 🌟 **EchoNext: The Future of Web** 🚀
<a id="readme-top"></a> 

<div align="center">  
  <p align="center">
    EchoNext is a lightweight, fast and scalable web framework for Python
    <br />
    <a href="https://alexeev-prog.github.io/pyEchoNext/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#-why-choose-pyechonext">Why Choose pyEchoNext</a>
    ·
    <a href="#-key-features">Key Features</a>
    ·
    <a href="#-getting-started">Getting Started</a>
    ·
    <a href="#-usage-examples">Basic Usage</a>
    ·
    <a href="#-specifications">Specification</a>
    ·
    <a href="https://alexeev-prog.github.io/pyEchoNext/">Documentation</a>
    ·
    <a href="https://github.com/alexeev-prog/pyEchoNext/blob/main/LICENSE">License</a>
  </p>
</div>
<br>
<p align="center">
    <img src="https://img.shields.io/github/languages/top/alexeev-prog/pyEchoNext?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/count/alexeev-prog/pyEchoNext?style=for-the-badge">
    <img src="https://img.shields.io/github/license/alexeev-prog/pyEchoNext?style=for-the-badge">
    <img src="https://img.shields.io/github/stars/alexeev-prog/pyEchoNext?style=for-the-badge">
    <img src="https://img.shields.io/github/issues/alexeev-prog/pyEchoNext?style=for-the-badge">
    <img src="https://img.shields.io/github/last-commit/alexeev-prog/pyEchoNext?style=for-the-badge">
    <img src="https://img.shields.io/pypi/wheel/pyechonext?style=for-the-badge">
    <img src="https://img.shields.io/badge/coverage-73%25-73%25?style=for-the-badge" alt="Coverage">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/pyEchoNext?style=for-the-badge">
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/pyEchoNext?style=for-the-badge">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pyEchoNext?style=for-the-badge">
    <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/alexeev-prog/pyEchoNext?style=for-the-badge">
</p>

<p align="center">
    <img src="https://raw.githubusercontent.com/alexeev-prog/pyEchoNext/refs/heads/main/docs/pallet-0.png">
</p>

**PyEchoNext** is a lightweight, high-performance web framework designed for building scalable Python web applications and APIs. With its modular architecture and focus on developer productivity, it combines Flask-like simplicity with FastAPI-inspired performance features. Built for modern web development challenges.

 > [!NOTE]
 > Python 3.12+

> [!CAUTION]
> PyEchoNext is currently in active alpha development. While core functionality is stable, some advanced features are still evolving. Production use requires thorough testing.

> [!NOTE]
> Versions below 0.7.14a are not recommended for use with gunicorn <23.0 due to the fact that they used an older version of gunicorn (<23.0), which was [vulnerable](https://deps.dev/advisory/osv/GHSA-hc5x-x2vx-497g).

 > Next big update: 0.8.0 - Hybrid Performance Core: async + multithread + multiprocess

You want see hybrid core before release? See [DevGuide Specs for HybridCore](./devguide/hybrid_core.md).

## Check Other My Projects

 + [SQLSymphony](https://github.com/alexeev-prog/SQLSymphony) - simple and fast ORM in sqlite (and you can add other DBMS)
 + [Burn-Build](https://github.com/alexeev-prog/burn-build) - simple and fast build system written in python for C/C++ and other projects. With multiprocessing, project creation and caches!
 + [OptiArch](https://github.com/alexeev-prog/optiarch) - shell script for fast optimization of Arch Linux
 + [libnumerixpp](https://github.com/alexeev-prog/libnumerixpp) - a Powerful C++ Library for High-Performance Numerical Computing
 + [pycolor-palette](https://github.com/alexeev-prog/pycolor-palette) - display beautiful log messages, logging, debugging.
 + [shegang](https://github.com/alexeev-prog/shegang) - powerful command interpreter (shell) for linux written in C

## 🤔 Why Choose pyEchoNext?

- **🔥 Featherweight Performance**: No bloat, just speed! Our framework is designed to optimize performance, making it a breeze to create and scale your applications without the overhead.
  
- **💼 Unmatched Scalability**: Handle thousands of connections effortlessly! Echonext is built for performance in high-demand environments, making it the perfect choice for startups or enterprise applications.

- **🔧 Customizable Architecture**: Tailor your framework to suit your unique needs. Whether it’s middleware, routing, or authentication, make it yours with minimal effort!

- **🌍 Cross-Platform Compatibility**: Echonext works beautifully on any OS. Whether you’re developing on Windows, macOS, or Linux, you’re covered!

- **💡 User-Friendly Design**: Our intuitive API and comprehensive documentation make it easy for beginners and pros alike. Dive in and start coding right away!

- **📦 Plug-and-Play Components**: Easily integrate with third-party libraries to enhance your application. Don’t reinvent the wheel—leverage existing solutions!

- **🔒 Built-in Authentication**: Simplify your user authentication process with our built-in, easy-to-implement features.

- **📊 Automatic API Documentation**: Create RESTful endpoints that are not just powerful but also well-documented, saving you time and effort.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📚 Key Features

- Intuitive API: Pythonic, object-oriented interface for interacting with routes and views.
- Performance Optimization: Lazy loading, eager loading, and other techniques for efficient web queries.
- Comprehensive Documentation: Detailed usage examples and API reference to help you get started.
- Modular Design: Clean, maintainable codebase that follows best software engineering practices.
- Extensive Test Coverage: Robust test suite to ensure the library's reliability and stability.

```mermaid
graph TD
    A[Router] --> B[Middleware]
    B --> C[Controllers]
    C --> D[Models]
    C --> E[Views]
    D --> F[Data]
    E --> G[Templates]
    A --> H[Static Files]
```


### Intelligent Routing System
- **Trie-based URL dispatch** - O(m) lookup complexity
- **Dynamic path parameters** - Type-annotated parameter handling
- **Nested routers** - Modular application organization

```python
# Hierarchical routing example
main_router = Router()
admin_router = Router(prefix="/admin")

@admin_router.route_page("/dashboard")
def admin_dashboard(request, response):
    return render_template("admin.html")

main_router.include_router(admin_router)
```

### Security Framework
- **Multi-layer protection**:
  - CSRF tokens with session binding
  - XSS double-escaping (content + attributes)
  - SQL injection pattern filtering
  - Rate limiting (sliding window algorithm)
- **Cryptographic modules**:
  - PSPCAlgorithm for lightweight encryption
  - SHA3/BLAKE3 hashing support
  - Salted password handling

```python
# Security implementation example
token = Security.generate_csrf_token(session_id)
filtered_query = Security.filter_sql_query("SELECT * FROM users; DROP TABLE users")
```

### ⚡ Performance Optimization
- **Multi-layer caching**:
  - LRU in-memory cache
  - Performance-optimized memoization
  - Static file preloading
- **JIT-friendly design**:
  - Numba-compatible critical paths
  - Zero-copy request processing
  - Async-ready architecture (in development)

```python
# Performance-cached view
@performance_cached(perf_cache)
def compute_intensive_view():
    return calculate_fibonacci(1000)
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## ⚙️ Functionality

 + i18n/l10n localization with [hermes-langlib](https://github.com/alexeev-prog/hermes_langlib).
 + basic project documentation generator
 + request/response
 + middlewares (with basic session cookie middleware)
 + views and routes
 + settings and config loader
 + built-in template engine and Jinja2
 + basic security and hashing
 + static files management
 + cache response bodies
 + performance
 + slugger
 + permissions
 + pyEchoNext Schemas (`pyechonext.schemas`) and pydantic support for validating schemas

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🚀 Getting Started

pyEchoNext is available on [PyPI](https://pypi.org/project/pyechonext). Simply install the package into your project environment with PIP:

```bash
pip install pyechonext
```

Once installed, you can start using the library in your Python projects. Check out the [documentation](https://alexeev-prog.github.io/pyEchoNext) for detailed usage examples and API reference.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## ⚙️ Dependency Injection
pyEchoNext is universal, and you are free to use any Dependency-Injection framework. But we recommend using the specially developed [echonextdi](https://github.com/alexeev-prog/echonext_di). It is simple and fast to use.

Install:

```bash
pip install echonextdi
```

Example code:

```python
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
```

## 💻 Usage Examples
You can view examples at [examples directory](./examples).

### Prefix Tree (Trie)
Prefix Tree data structure (this structure also used in pyechonext routing system)

```python
from pyechonext.utils.trie import  PrefixTree

if __name__ == '__main__':
    trie = PrefixTree()
    trie.insert('apple')
    trie.insert('app')
    trie.insert('aposematic')
    trie.insert('appreciate')
    trie.insert('book')
    trie.insert('bad')
    trie.insert('bear')
    trie.insert('bat')
    print(trie.starts_with('app'))

    router_tree = PrefixTree()
    router_tree.insert('index')
    router_tree.insert('users')
    router_tree.insert('transactions')
    router_tree.insert('wallets')
    router_tree.insert('wallets/create')

    print(router_tree.starts_with('wa'))

```

### i18n with hermes-langlib
Hermes LangLib - a fast and light python library for translating, localizing and internationalizing your applications. The library is aimed at high speed and stability; it can be used in highly loaded projects.

Directory tree:

```
├── example.toml
└── locales
    └── default.json
```

Example config-file `example.toml`:

```toml
locale_directory="locales"
default_locale_file="default.json"
default_language="RU_RU"
translator="google"
```

Example locale file `locales/default.json`:

```json
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
```

Example usage:

```python
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
```

You can read [Hermes-Langlib Specification at this link](https://github.com/alexeev-prog/hermes_langlib/tree/main?tab=readme-ov-file#-specifications).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Basic With Depends Injection

```python
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

```

### Performance caching

```python
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
```

### Permissions

```python
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
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🔧 Specifications

### Security
A security module created for hash functions and crypto-algorithms.

#### Crypts
Simple crypto-algorithms.

##### PSPCAlgorithm
Point Simple Password Crypt Algorithm.

```
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
```

Example:

```python
from pyechonext.security.crypts import PSPCAlgorithm


pspc = PSPCAlgorithm()

passwords = ['AngryPassword', 'S0mesd7623tds@&6^@_', 'PassWord', 'Pass']

for password in passwords:
    print('Base:', password)
    print('Crypted:', pspc.crypt(password))
    print('Decrypted:', pspc.decrypt(pspc.crypt(password)))
    print()
```

#### Hashing
 
 + Module: `pyechonext.security.hashing`

##### HashAlgorithm
Enum class with available hashing algorithms

```python
class HashAlgorithm(Enum):
    """
    This class describes a hash algorithms.
    """

    SHA256 = auto()
    SHA512 = auto()
    MD5 = auto()
    BLAKE2B = auto()
    BLAKE2S = auto()
```

##### PlainHasher
A simple class for hashing text. Has no 'salting'.

```python
hasher = PlainHasher(HashAlgorithm.BLAKE2S)
old_hash = hasher.hash("TEXT")
new_hash = hasher.hash("TEXT")

if hasher.verify("TEXT", new_hash): # true
    print('Yes!')

if hasher.verify("TEXT2", old_hash): # false
    print('Yes!')

# Output: one "Yes!"
```

##### SaltedHasher
A simple class for hashing text. Has hash salt.

```python
hasher = SaltedHasher(HashAlgorithm.BLAKE2S, salt='bob')
old_hash = hasher.hash("TEXT")
new_hash = hasher.hash("TEXT")

if hasher.verify("TEXT", new_hash): # true
    print('Yes!')

if hasher.verify("TEXT2", old_hash): # false
    print('Yes!')

# Output: one "Yes!"
```

### View
View is an abstract class, with abstract get and post methods (all descendants must create these methods).

```python
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
```

Example of view:

```python
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
```

Or you can return response:

```python
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
```

## Tests coverage
To test the web framework, PyTest with the pytest-cov plugin is used. You can look at the tests in [tests directory](./tests)

## Documentation 🌍
The main documentation is [here](https://alexeev-prog.github.io/pyEchoNext/).

<img src="https://github.com/alexeev-prog/pyEchoNext/actions/workflows/docs.yml/badge.svg">

## 💬 Support
If you encounter any issues or have questions about pyEchoNext, please:

- Check the [documentation](https://alexeev-prog.github.io/pyEchoNext) for answers
- Open an [issue on GitHub](https://github.com/alexeev-prog/pyEchoNext/issues/new)
- Reach out to the project maintainers via the [mailing list](mailto:alexeev.dev@mail.ru)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🤝 Contributing
We welcome contributions from the community! If you'd like to help improve pyEchoNext, please check out the [contributing guidelines](https://github.com/alexeev-prog/pyEchoNext/blob/main/CONTRIBUTING.md) to get started.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 👥 Join the Community!
If you find Echonext valuable and want to support the project:

- Star on GitHub ⭐
- Share it with friends and colleagues!
- Donate via cryptocurrency 🙌

Connect with fellow Echonext users: [Join our Telegram Chat](https://t.me/pyEchoNext_Forum)

## Roadmap & Future Development

### Q2-Q3 2025
- [x] **0.8.0**: Hybrid core: async + multithread + multiprocess
- [ ] Database ORM integration
- [ ] OpenAPI 3.1 schema generation
- [ ] Built-in monitoring dashboard

### Q3-Q4 2025
- [ ] JWT authentication module
- [ ] Websocket support
- [ ] Distributed task queue
- [ ] GRPC integration

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributor Guidelines

We welcome PRs addressing:
- Security enhancements
- Performance optimization
- Documentation improvements
- Test coverage expansion
- ASGI migration path

**Before contributing**:
1. Review [docs](https://alexeev-prog.github.io/pyEchoNext/)
2. Maintain 100% test coverage for new code
3. Follow PEP8 and SOLID, DRY, KISS principles
4. Include type annotations

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### License & Support
This project operates under **GNU LGPL 2.1** - see [LICENSE](https://github.com/alexeev-prog/pyEchoNext/blob/main/LICENSE). For enterprise support, contact [alexeev.dev@mail.ru](mailto:alexeev.dev@mail.ru).

**PyEchoNext** - Build robust web applications with Pythonic elegance.  

[Explore Documentation](https://alexeev-prog.github.io/pyEchoNext) | 
[Report Issue](https://github.com/alexeev-prog/pyEchoNext/issues) | 
[View Examples](/examples)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

EchoNext is a lightweight, fast and scalable web framework for Python
Copyright (C) 2024  Alexeev Bronislav (C) 2024

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
USA
