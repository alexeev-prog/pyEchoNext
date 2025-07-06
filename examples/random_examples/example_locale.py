from pyechonext.apidoc_ui import APIDocUI, APIDocumentation
from pyechonext.app import ApplicationType, EchoNext
from pyechonext.config import SettingsConfigType, SettingsLoader
from pyechonext.middleware import middlewares
from pyechonext.mvc.controllers import PageController
from pyechonext.static import StaticFile
from pyechonext.template_engine.jinja import render_template
from pyechonext.urls import URL
from pyechonext.utils.exceptions import MethodNotAllow


class UsersView(PageController):
    def get(self, request, response, *args, **kwargs):
        return render_template(
            request,
            "index.html",
            user_name="User",
            session_id=request.session_id,
            friends=["Bob", "Anna", "John"],
        )

    def post(self, request, response, *args, **kwargs):
        raise MethodNotAllow(f"Request {request.path}: method not allow")


url_patterns = [URL(path="/users", controller=UsersView)]
config_loader = SettingsLoader(SettingsConfigType.PYMODULE, "el_config.py")
settings = config_loader.get_settings()
static_files = [StaticFile(settings, "styles.css")]
echonext = EchoNext(
    __name__,
    settings,
    middlewares,
    urls=url_patterns,
    application_type=ApplicationType.HTML,
    static_files=static_files,
)
apidoc = APIDocumentation(echonext)


@echonext.route_page("/api-docs")
def api_docs(request, response):
    ui = APIDocUI(apidoc.generate_spec())
    return ui.generate_html_page()


@echonext.route_page("/book")
class BooksResource(PageController):
    """
    This class describes a books resource.
    """

    def get(self, request, response, **kwargs):
        """
        Get queries

        :param		request:   The request
        :type		request:   Request
        :param		response:  The response
        :type		response:  Response
        :param		kwargs:	   The keywords arguments
        :type		kwargs:	   dictionary

        :returns:	result
        :rtype:		str
        """
        return echonext.i18n_loader.get_string("title %{name}", name=str(request.GET))

    def post(self, request, response, **kwargs):
        """
        Post queries

        :param		request:   The request
        :type		request:   Request
        :param		response:  The response
        :type		response:  Response
        :param		kwargs:	   The keywords arguments
        :type		kwargs:	   dictionary

        :returns:	result
        :rtype:		str
        """
        return echonext.l10n_loader.format_currency(1305.50)
