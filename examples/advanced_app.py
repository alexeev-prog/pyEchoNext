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
