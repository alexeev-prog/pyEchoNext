import os

from pyechonext.app import ApplicationType, EchoNext
from pyechonext.config import Settings
from pyechonext.middleware import middlewares
from pyechonext.mvc.controllers import PageController
from pyechonext.response import Response
from pyechonext.urls import URL


class UsersPageController(PageController):
    def get(self, request, response, **kwargs):
        return Response(request, body={"users": "get"})

    def post(self, request, response, **kwargs):
        return {"users": "post"}


url_patterns = [URL(path="/users", controller=UsersPageController)]

settings = Settings(
    BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"
)

echonext = EchoNext(
    __name__,
    settings,
    middlewares,
    urls=url_patterns,
    application_type=ApplicationType.JSON,
)


@echonext.route_page("/{name}/")
def index(request, response, name):
    return name


@echonext.route_page("/book")
class BooksResource(PageController):
    def get(self, request, response, **kwargs):
        return {"params": request.GET, "page": "books"}

    def post(self, request, response, **kwargs):
        return {"params": request.POST, "page": "books"}
