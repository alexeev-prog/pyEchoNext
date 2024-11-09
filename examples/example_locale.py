import os
from pyechonext.utils.exceptions import MethodNotAllow
from pyechonext.app import ApplicationType, EchoNext
from pyechonext.views import View
from pyechonext.urls import URL, IndexView
from pyechonext.config import SettingsLoader, SettingsConfigType
from pyechonext.response import Response
from pyechonext.template_engine.jinja import render_template
from pyechonext.middleware import middlewares
from pyechonext.docsgen import ProjDocumentation


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
config_loader = SettingsLoader(SettingsConfigType.PYMODULE, 'el_config.py')
settings = config_loader.get_settings()
echonext = EchoNext(
	__name__,
	settings,
	middlewares,
	urls=url_patterns,
	application_type=ApplicationType.HTML,
)
apidoc = ProjDocumentation(echonext)


@echonext.route_page("/book")
@apidoc.documentate_route('/book', str, {}, ['GET', 'POST'])
class BooksResource(View):
	"""
	This class describes a books resource.
	"""

	def get(self, request, response, **kwargs):
		"""
		get queries

		:param      request:   The request
		:type       request:   Request
		:param      response:  The response
		:type       response:  Response
		:param      kwargs:    The keywords arguments
		:type       kwargs:    dictionary

		:returns:   result
		:rtype:     str
		"""
		return Response(request, body="title", use_i18n=True)

	def post(self, request, response, **kwargs):
		"""
		post queries

		:param      request:   The request
		:type       request:   Request
		:param      response:  The response
		:type       response:  Response
		:param      kwargs:    The keywords arguments
		:type       kwargs:    dictionary

		:returns:   result
		:rtype:     str
		"""
		return f"POST Params: {request.POST}"


apidoc.generate_documentation()
