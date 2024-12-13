import os

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
def hello(request, response, name: str = "World"):
	response.body = f"Hello {name}!"
