import os
from pyechonext.app import ApplicationType, EchoNext
from pyechonext.views import View
from pyechonext.urls import URL, IndexView
from pyechonext.response import Response
from pyechonext.config import Settings


class UsersView(View):
	def get(self, request, response, **kwargs):
		return Response(body={"users": "get"})

	def post(self, request, response, **kwargs):
		return {"users": "post"}


url_patterns = [URL(url="/", view=IndexView), URL(url="/users", view=UsersView)]

settings = Settings(
	BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"
)

echonext = EchoNext(
	__name__, settings, urls=url_patterns, application_type=ApplicationType.JSON
)


@echonext.route_page("/book")
class BooksResource(View):
	def get(self, request, response, **kwargs):
		return {"params": {request.GET}, "page": "books"}

	def post(self, request, response, **kwargs):
		return {"params": {request.POST}, "page": "books"}
