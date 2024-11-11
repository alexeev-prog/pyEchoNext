

class APIDocumentation:
	"""
	This class describes an API documentation.
	"""

	def __init__(self, app: "EchoNext"):
		"""
		Constructs a new instance.

		:param		app:  The application
		:type		app:  EchoNext
		"""
		self._app = app

	def init_app(self, app: "EchoNext"):
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
			spec["paths"][url.url] = {
				"get": {
					"summary": str(url.view.__doc__).strip().replace('\n', '.').replace('\t', ';'),
					"responses": {"200": {"description": "Successful response"}},
				}
			}

		for path, handler in self._app.routes.items():
			spec["paths"][path] = {
				"get": {
					"summary": str(handler.__doc__).strip().replace('\n', '.').replace('\t', ';'),
					"responses": {"200": {"description": "Successful response"}},
				}
			}

		return spec
