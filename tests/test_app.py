import os

import pytest

from pyechonext.app import ApplicationType, EchoNext
from pyechonext.config import Settings
from pyechonext.middleware import middlewares
from pyechonext.mvc.controllers import PageController


@pytest.fixture
def echonext():
	settings = Settings(
		BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"
	)
	echonext = EchoNext(
		__name__,
		settings,
		middlewares,
		application_type=ApplicationType.HTML,
	)
	return echonext


@pytest.fixture
def client(echonext):
	return echonext.test_session()


def test_basic_route(echonext, client):
	RESPONSE_TEXT = "Hello World"

	@echonext.route_page("/")
	def index(request, response):
		response.body = RESPONSE_TEXT

	@echonext.route_page("/hello/{name}")
	def hello(request, response, name):
		response.body = f"hey {name}"

	@echonext.route_page("/title")
	def title(request, response):
		return echonext.i18n_loader.get_string("title %{name}", name="Test")

	@echonext.route_page("/books")
	class BooksController(PageController):
		def get(self, request, response, **kwargs):
			return "Book Get"

		def post(self, request, response, **kwargs):
			return "Book Post"

	assert client.get("http://echonext/").text == RESPONSE_TEXT
	assert client.get("http://echonext/hello/matthew").text == "hey matthew"
	assert client.get("http://echonext/hello/ashley").text == "hey ashley"
	assert client.get("http://echonext/books").text == "Book Get"
	assert client.post("http://echonext/books").text == "Book Post"
	assert client.get("http://echonext/title").text == "pyEchoNext Example Website Test"
