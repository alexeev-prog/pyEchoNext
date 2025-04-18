import os

from echonextdi.containers.container import Container
from echonextdi.depends import Depends
from echonextdi.providers.callable_provider import CallableProvider

from pyechonext.app import ApplicationType, EchoNext
from pyechonext.config import Settings
from pyechonext.middleware import middlewares
from pyechonext.mvc.controllers import PageController
from pyechonext.urls import URL


class IndexController(PageController):
	def get(self, request, response, **kwargs):
		return "Hello"

	def post(self, request, response, **kwargs):
		return "Hello"


def say_hello(name: str, phrase: str = "Hello"):
	return f"{phrase} {name}"


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
def hello(
	request,
	response,
	name: str = "World",
	depend: Depends = Depends(container, Hello_Dependency),
):
	response.body = depend().say_hello(name)
