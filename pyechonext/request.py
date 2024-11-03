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
		self.environ: dict = environ
		self.settings: Settings = settings
		self.method: str = self.environ["REQUEST_METHOD"]
		self.path: str = self.environ["PATH_INFO"]
		self.GET: dict = self._build_get_params_dict(self.environ["QUERY_STRING"])
		self.POST: dict = self._build_post_params_dict(
			self.environ["wsgi.input"].read()
		)
		self.user_agent: str = self.environ["HTTP_USER_AGENT"]
		self.extra: dict = {}

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

	def _build_get_params_dict(self, raw_params: str):
		"""
		Builds a get parameters dictionary.

		:param		raw_params:	 The raw parameters
		:type		raw_params:	 str
		"""
		return parse_qs(raw_params)

	def _build_post_params_dict(self, raw_params: bytes):
		"""
		Builds a post parameters dictionary.

		:param		raw_params:	 The raw parameters
		:type		raw_params:	 bytes
		"""
		return parse_qs(raw_params.decode())
