# EchoNext
<a id="readme-top"></a> 

<div align="center">  
  <p align="center">
	EchoNext is a lightweight, fast and scalable web framework for Python
	<br />
	<a href="https://alexeev-prog.github.io/pyEchoNext/"><strong>Explore the docs »</strong></a>
	<br />
	<br />
	<a href="#-comparison-with-alternatives">Comparison with Alternatives</a>
	.
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
</p>

 > EchoNext is a lightweight, fast and scalable web framework for Python

Welcome to **EchoNext**, where innovation meets simplicity! Are you tired of the sluggishness of traditional web frameworks? Want a solution that keeps pace with your ambitious apps? Look no further. EchoNext is your agile companion in the world of web development!

**Imagine** a lightweight framework that empowers you to create modern web applications with lightning speed and flexibility. With EchoNext, you're not just coding; you're building a masterpiece!

## 🚀 Getting Started

pyEchoNext is available on [PyPI](https://pypi.org/project/pyechonext). Simply install the package into your project environment with PIP:

```bash
pip install pyechonext
```

Once installed, you can start using the library in your Python projects. Check out the [documentation](https://alexeev-prog.github.io/pyEchoNext) for detailed usage examples and API reference.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Advanced app with flask-like and django-like routes
Index page and book

```python
from pyechonext.app import ApplicationType, EchoNext
from pyechonext.views import View
from pyechonext.urls import url_patterns


echonext = EchoNext(url_patterns, __name__, application_type=ApplicationType.HTML)


@echonext.route_page("/book")
class BooksResource(View):
	def get(self, request, response, **kwargs):
		return f"Books Page: {request.query_params}"

	def post(self, request, response, **kwargs):
		return "Endpoint to create a book"
```

### Simple app with database
In this example we are using SQLSymphony ORM (our other project, a fast and simple ORM for python)

```python
from pyechonext.app import ApplicationType, EchoNext
from sqlsymphony_orm.datatypes.fields import IntegerField, RealField, TextField
from sqlsymphony_orm.models.session_models import SessionModel
from sqlsymphony_orm.models.session_models import SQLiteSession
from sqlsymphony_orm.queries import QueryBuilder


echonext = EchoNext(__name__, application_type=ApplicationType.HTML)
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
	user = User(name='John', cash=100.0)
	session.add(user)
	session.commit()
	response.body = "Hello from the HOME page"


@echonext.route_page("/users")
def about(request, response):
	users = session.get_all_by_model(User)
	
	response.body = f"Users: {[f'{user.name}: {user.cash}$' for user in users]}"
```

## 💬 Support
If you encounter any issues or have questions about pyEchoNext, please:

- Check the [documentation](https://alexeev-prog.github.io/pyEchoNext) for answers
- Open an [issue on GitHub](https://github.com/alexeev-prog/pyEchoNext/issues/new)
- Reach out to the project maintainers via the [mailing list](mailto:alexeev.dev@mail.ru)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🤝 Contributing
We welcome contributions from the community! If you'd like to help improve pyEchoNext, please check out the [contributing guidelines](https://github.com/alexeev-prog/pyEchoNext/blob/main/CONTRIBUTING.md) to get started.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🔮 Roadmap
Our future goals for pyEchoNext include:

- 📚 Improve middlewares
- 🚀 Add async support
- ✅ Improve logging
- 🌍 Improve auth
- 🌐 More stability and scalablity

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License
Distributed under the GNU LGPL 2.1 License. See [LICENSE](https://github.com/alexeev-prog/pyEchoNext/blob/main/LICENSE) for more information.

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
