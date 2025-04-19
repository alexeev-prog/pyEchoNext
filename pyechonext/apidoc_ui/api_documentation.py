from pyechonext.app import EchoNext


class APIDocumentation:
    """
    This class describes an API documentation.
    """

    def __init__(self, app: EchoNext):
        """
        Constructs a new instance.

        :param		app:  The application
        :type		app:  EchoNext
        """
        self._app = app

    def init_app(self, app: EchoNext):
        """
        Initializes the application.

        :param		app:  The application
        :type		app:  EchoNext
        """
        self._app = app

    def generate_spec(self) -> str:
        """
        Generate OpenAPI specficiation from app routes&views

        :returns:	jsonfied openAPI API specification
        :rtype:		str
        """
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": self._app.app_name,
                "version": self._app.settings.VERSION,
                "description": self._app.settings.DESCRIPTION,
            },
            "paths": {},
        }

        for url in self._app.urls:
            spec["paths"][url.path] = {
                "get": {
                    "summary": str(
                        f"{url.controller.__doc__}: {url.controller.get.__doc__}"
                        if url.summary is None
                        else url.summary
                    )
                    .replace("\n", "<br>")
                    .strip(),
                    "responses": {
                        "200": {"description": "Successful response"},
                        "405": {"description": "Method not allow"},
                    },
                },
                "post": {
                    "summary": str(
                        f"{url.controller.__doc__}: {url.controller.post.__doc__}"
                        if url.summary is None
                        else url.summary
                    ).replace("\n", "<br>"),
                    "responses": {
                        "200": {"description": "Successful response"},
                        "405": {"description": "Method not allow"},
                    },
                },
            }

        for path, router in self._app.router.routes.items():
            spec["paths"][path] = {
                "get": {
                    "summary": (
                        str(
                            router.handler.get.__doc__
                            if not callable(router.handler)
                            else router.handler.__doc__
                        )
                        if router.summary is None
                        else router.summary
                    ),
                    "responses": {
                        "200": {"description": "Successful response"},
                        "405": {"description": "Method not allow"},
                    },
                },
                "post": {
                    "summary": (
                        str(
                            router.handler.post.__doc__
                            if not callable(router.handler)
                            else router.handler.__doc__
                        )
                        if router.summary is None
                        else router.summary
                    ),
                    "responses": {
                        "200": {"description": "Successful response"},
                        "405": {"description": "Method not allow"},
                    },
                },
            }

        return spec
