import json
from typing import Dict, Iterable
from socks import method
from loguru import logger


class Response:
	"""
	This dataclass describes a response.
	"""

	default_content_type = "application/json"
	default_charset = "UTF-8"
	unicode_errors = "strict"
	default_conditional_response = False
	default_body_encoding = "UTF-8"

	def __init__(
		self,
		status_code: int = 200,
		body: str = None,
		headers: Dict[str, str] = {},
		content_type: str = None,
		charset: str = None,
	):
		"""
		Constructs a new instance.

		:param		status_code:   The status code
		:type		status_code:   int
		:param		body:		   The body
		:type		body:		   str
		:param		headers:	   The headers
		:type		headers:	   Dict[str, str]
		:param		content_type:  The content type
		:type		content_type:  str
		"""
		if status_code == 200:
			self.status_code = "200 OK"
		else:
			self.status_code = str(status_code)

		if content_type is None:
			self.content_type = self.default_content_type
		else:
			self.content_type = content_type

		if charset is None:
			self.charset = self.default_charset
		else:
			self.charset = charset

		if body is not None:
			self.body = body.encode()
		else:
			self.body = b""

		self._headerslist = headers
		self.headers = [
			("Content-Type", f"{self.content_type}; charset={self.charset}")
		]

		self._structuring_headers()

	def _structuring_headers(self):
		for header_name, header_value in self._headerslist.items():
			self.headers.append((header_name, header_value))

	@property
	def json(self) -> dict:
		"""
		Parse request body as JSON.

		:returns:	json body
		:rtype:		dict
		"""
		if self.body:
			if self.content_type.split("/")[-1] == "json":
				return json.loads(self.body.decode())
			else:
				return json.loads(json.dumps(self.body.decode()))

		return {}

	def __call__(self, environ: dict, start_response: method) -> Iterable:
		"""
		Makes the Response object callable.

		:param		environ:		 The environ
		:type		environ:		 dict
		:param		start_response:	 The start response
		:type		start_response:	 method

		:returns:	response body
		:rtype:		Iterable
		"""
		self.body = self.body.encode()

		self.headers.append(("User-Agent", environ["HTTP_USER_AGENT"]))
		self.headers.append(("Content-Length", str(len(self.body))))

		logger.debug(
			f"[{environ['REQUEST_METHOD']} {self.status_code}] Run response: {self.content_type}"
		)
		start_response(status=self.status_code, headers=self.headers)

		return iter([self.body])

	def __repr__(self):
		return f"<{self.__class__.__name__} at 0x{abs(id(self)):x} {self.status_code}>"
