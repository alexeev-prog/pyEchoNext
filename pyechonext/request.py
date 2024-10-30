import json
from typing import Any, Union
from urllib.parse import parse_qs
from loguru import logger
from pyechonext.config import Settings


class Request:
	"""
	This class describes a request.
	"""

	def __init__(self, environ: dict, settings: Settings):
		"""
		Constructs a new instance.

		:param		environ:  The environ
		:type		environ:  dict
		"""
		self.environ = environ
		self.settings = settings
		self.method = self.environ["REQUEST_METHOD"]
		self.path = self.environ["PATH_INFO"]
		self.build_get_params_dict(self.environ["QUERY_STRING"])
		self.build_post_params_dict(self.environ["wsgi.input"].read())
		self.user_agent = self.environ["HTTP_USER_AGENT"]
		self.extra = {}

		logger.debug(f"New request created: {self.method} {self.path}")

	def __getattr__(self, item: Any) -> Union[Any, None]:
		"""
		Magic method for get attrs (from extra)

		:param		item:  The item
		:type		item:  Any

		:returns:	Item from self.extra or None
		:rtype:		Union[Any, None]
		"""
		return self.extra.get(item, None)

	def build_get_params_dict(self, raw_params: str):
		"""
		Builds a get parameters dictionary.

		:param		raw_params:	 The raw parameters
		:type		raw_params:	 str
		"""
		self.GET = parse_qs(raw_params)

	def build_post_params_dict(self, raw_params: bytes):
		"""
		Builds a post parameters dictionary.

		:param		raw_params:	 The raw parameters
		:type		raw_params:	 bytes
		"""
		self.POST = parse_qs(raw_params.decode())

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
