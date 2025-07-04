from pyechonext.app import EchoNext


class APIDocumentation:
    """
    This class describes an API documentation.
    """

    def __init__(self, app: EchoNext):
        """Constructs a new instance

        Args:
            app (Optional[EchoNext]): echonext WSGI app. Defaults to None.
        """
        self._app: EchoNext = app

    def init_app(self, app: EchoNext):
        """Initialize application

        Args:
            app (EchoNext): echonext WSGI app
        """
        self._app = app

    def generate_spec(self) -> dict:
        """Generate simple OpenAPI configuration from routes

        Returns:
            dict: openapi configuration
        """
        if not isinstance(self._app, EchoNext):
            raise AttributeError(
                f"Unknown application type: {type(self._app)}")

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
                    "summary": (
                        str(
                            f"{url.controller.__doc__}: {url.controller.get.__doc__}"
                            if url.summary is None
                            else url.summary
                        )
                        .replace("\n", "<br>")
                        .strip()
                    ),
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
