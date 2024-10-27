import json
from loguru import logger


class Request:
	"""
	This class describes a request.
	"""

	def __init__(self, environ: dict):
		"""
		Constructs a new instance.

		:param		environ:  The environ
		:type		environ:  dict
		"""
		self.environ = environ
		self.method = self.environ["REQUEST_METHOD"]
		self.path = self.environ["PATH_INFO"]
		self.query_params = self.environ["QUERY_STRING"]
		self.body = self.environ["wsgi.input"].read().decode()
		self.user_agent = self.environ["HTTP_USER_AGENT"]

		logger.debug(f"New request created: {self.method} {self.path}")

	@property
	def json(self) -> dict:
		"""
		Parse request body as JSON.

		:returns:	json body
		:rtype:		dict
		"""
		if self.body:
			return json.loads(json.dumps(self.body.decode()))

		return {}
