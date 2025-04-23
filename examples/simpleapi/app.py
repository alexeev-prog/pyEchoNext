import os
from random import randint

from pyechonext.app import ApplicationType, EchoNext
from pyechonext.config import Settings
from pyechonext.middleware import middlewares
from pyechonext.mvc.controllers import PageController
from pyechonext.mvc.routes import Router
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

router = Router(prefix="/users")


@router.route_page("/create", methods=["POST"], summary="create user")
def create_user(request, response):
    return {"status": "user created", "username": request.POST.get("username")}


@router.route_page("/get", methods=["GET"], summary="get user")
def get_user(request, response):
    return {"status": randint(1, 1000), "params": request.GET}


echonext.include_router(router)
