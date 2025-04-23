from pyechonext.apidoc_ui import APIDocUI, APIDocumentation
from pyechonext.app import ApplicationType, EchoNext
from pyechonext.config import SettingsConfigType, SettingsLoader
from pyechonext.logging import logger
from pyechonext.middleware import middlewares
from pyechonext.mvc.controllers import PageController
from pyechonext.template_engine.jinja import render_template
from pyechonext.urls import URL
from pyechonext.utils.exceptions import MethodNotAllow
from pyechonext.static import StaticFile


class UsersView(PageController):
    def get(self, request, response, **kwargs):
        logger.info("BOB USERS ANAN")
        return render_template(
            request,
            "index.html",
            user_name="User",
            session_id=request.session_id,
            friends=["Bob", "Anna", "John"],
        )

    def post(self, request, response, **kwargs):
        raise MethodNotAllow(f"Request {request.path}: method not allow")


url_patterns = [
    URL(path="/", controller=UsersView),
]
config_loader = SettingsLoader(SettingsConfigType.PYMODULE, "example_module.py")
settings = config_loader.get_settings()
echonext = EchoNext(
    __name__,
    settings,
    middlewares,
    static_files=[StaticFile(settings, 'styles.css')],
    urls=url_patterns,
    application_type=ApplicationType.HTML,
)
apidoc = APIDocumentation(echonext)


@echonext.route_page("/api-docs", summary="api docs")
def api_docs(request, response):
    ui = APIDocUI(apidoc.generate_spec())
    return ui.generate_html_page()


@echonext.route_page("/book", summary="books")
class BooksResource(PageController):
    """
    This class describes a books resource.
    """

    def get(self, request, response, **kwargs):
        """
        get queries

        :param		request:   The request
        :type		request:   Request
        :param		response:  The response
        :type		response:  Response
        :param		kwargs:	   The keywords arguments
        :type		kwargs:	   dictionary

        :returns:	result
        :rtype:		str
        """
        return f"GET Params: {request.GET}"

    def post(self, request, response, **kwargs):
        """
        post queries

        :param		request:   The request
        :type		request:   Request
        :param		response:  The response
        :type		response:  Response
        :param		kwargs:	   The keywords arguments
        :type		kwargs:	   dictionary

        :returns:	result
        :rtype:		str
        """
        return f"POST Params: {request.POST}"
