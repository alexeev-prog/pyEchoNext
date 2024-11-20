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
from pyechonext.apidoc_ui import APIDocumentation, APIDocUI


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
apidoc = APIDocumentation(echonext)
projdoc = ProjDocumentation(echonext)


@echonext.route_page('/api-docs')
def api_docs(request, response):
	ui = APIDocUI(apidoc.generate_spec())
	return ui.generate_html_page()


@echonext.route_page("/book")
@projdoc.documentate_route('/book', str, {}, ['GET', 'POST'])
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
		return echonext.i18n_loader.get_string('title %{name}', name=str(request.GET))

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
		return echonext.l10n_loader.format_currency(1305.50)


projdoc.generate_documentation()
