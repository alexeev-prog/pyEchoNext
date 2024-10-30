import os
from pyechonext.utils.exceptions import MethodNotAllow
from pyechonext.app import ApplicationType, EchoNext
from pyechonext.views import View
from pyechonext.urls import URL, IndexView
from pyechonext.config import Settings
from pyechonext.template_engine.jinja import render_template
from pyechonext.middleware import middlewares


class UsersView(View):
	def get(self, request, response, **kwargs):
		return render_template(
			request,
			"index.html",
			user_name="User",
			session_id=request.session_id,
			friends=["Bob", "Anna", "John"],
		)

	def post(self, request, response, **kwargs):
		raise MethodNotAllow(f"Request {request.path}: method not allow")


url_patterns = [URL(url="/", view=IndexView), URL(url="/users", view=UsersView)]
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


@echonext.route_page("/book")
class BooksResource(View):
	def get(self, request, response, **kwargs):
		return f"GET Params: {request.GET}"

	def post(self, request, response, **kwargs):
		return f"POST Params: {request.POST}"
