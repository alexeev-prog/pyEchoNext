from abc import ABC, abstractmethod
from uuid import uuid4
from urllib.parse import parse_qs
from loguru import logger
from pyechonext.response import Response
from pyechonext.request import Request


class BaseMiddleware(ABC):
	"""
	This abstract class describes a base middleware.
	"""

	@abstractmethod
	def to_request(self, request: Request):
		"""
		To request method

		:param		request:  The request
		:type		request:  Request
		"""
		raise NotImplementedError

	@abstractmethod
	def to_response(self, response: Response):
		"""
		To response method

		:param		response:  The response
		:type		response:  Response
		"""
		raise NotImplementedError


class SessionMiddleware(BaseMiddleware):
	"""
	This class describes a session (cookie) middleware.
	"""

	def to_request(self, request: Request):
		"""
		Set to request

		:param		request:  The request
		:type		request:  Request
		"""
		cookie = request.environ.get("HTTP_COOKIE", None)

		if not cookie:
			return

		session_id = parse_qs(cookie)["session_id"][0]
		logger.debug(
			f"Set session_id={session_id} for request {request.method} {request.path}"
		)
		request.extra["session_id"] = session_id

	def to_response(self, response: Response):
		"""
		Set to response

		:param		response:  The response
		:type		response:  Response
		"""
		if not response.request.session_id:
			session_id = uuid4()
			logger.debug(
				f"Set session_id={session_id} for response {response.status_code} {response.request.path}"
			)
			response.add_headers(
				[
					("Set-Cookie", f"session_id={session_id}"),
				]
			)


middlewares = [SessionMiddleware]
