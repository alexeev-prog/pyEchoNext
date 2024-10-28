from pyechonext.app import ApplicationType, EchoNext
from pyechonext.views import View
from pyechonext.urls import URL, IndexView


class UsersView(View):
	def get(self, request, response, **kwargs):
		return "users get"

	def post(self, request, response, **kwargs):
		return "users post"


url_patterns = [URL(url="/", view=IndexView), URL(url="/users", view=UsersView)]

echonext = EchoNext(__name__, urls=url_patterns, application_type=ApplicationType.HTML)


@echonext.route_page("/book")
class BooksResource(View):
	def get(self, request, response, **kwargs):
		return f"Books Page: {request.query_params}"

	def post(self, request, response, **kwargs):
		return "Endpoint to create a book"
