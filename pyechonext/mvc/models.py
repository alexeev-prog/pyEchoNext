from typing import Any, Union
from abc import ABC, abstractmethod
from pyechonext.request import Request
from pyechonext.response import Response


class BaseModel(ABC):
	"""
	This class describes a base model.
	"""

	@abstractmethod
	def create_response(self, *args, **kwargs) -> Response:
		"""
		Creates a response.

		:param      args:    The arguments
		:type       args:    list
		:param      kwargs:  The keywords arguments
		:type       kwargs:  dictionary

		:returns:   response object
		:rtype:     Response
		"""
		raise NotImplementedError

	@abstractmethod
	def create_request(self, *args, **kwargs) -> Request:
		"""
		Creates a request.

		:param      args:    The arguments
		:type       args:    list
		:param      kwargs:  The keywords arguments
		:type       kwargs:  dictionary

		:returns:   request object
		:rtype:     Request
		"""
		raise NotImplementedError


class PageModel(BaseView):
	"""
	This class describes a page model.
	"""

	def __init__(self, request: Request, response: Response):
		"""
		Constructs a new instance.

		:param      request:   The request
		:type       request:   Request
		:param      response:  The response
		:type       response:  Response
		"""
		self.request = request
		self.response = response

	def create_response(self, *args, **kwargs) -> Response:
		"""
		Creates a response.

		:param      args:    The arguments
		:type       args:    list
		:param      kwargs:  The keywords arguments
		:type       kwargs:  dictionary

		:returns:   response object
		:rtype:     Response
		"""
		return Response(*args, **kwargs)

	def create_request(self, *args, **kwargs) -> Request:
		"""
		Creates a request.

		:param      args:    The arguments
		:type       args:    list
		:param      kwargs:  The keywords arguments
		:type       kwargs:  dictionary

		:returns:   request object
		:rtype:     Request
		"""
		return Request(*args, **kwargs)
