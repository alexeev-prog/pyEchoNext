from abc import ABC, abstractmethod
from pyechonext.request import Request
from pyechonext.response import Response


class View(ABC):
	"""
	Page view
	"""

	@abstractmethod
	def get(self, request: Request, response: Response, *args, **kwargs):
		"""
		Get

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		args:	   The arguments
		:type		args:	   list
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary
		"""
		raise NotImplementedError

	@abstractmethod
	def post(self, request: Request, response: Response, *args, **kwargs):
		"""
		Post

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		args:	   The arguments
		:type		args:	   list
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary
		"""
		raise NotImplementedError


class IndexView(View):
	def get(self, request: Request, response: Response, **kwargs):
		"""
		Get

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		args:	   The arguments
		:type		args:	   list
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary
		"""
		return "Hello World!"

	def post(self, request: Request, response: Response, **kwargs):
		"""
		Post

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		args:	   The arguments
		:type		args:	   list
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary
		"""
		return "Message has accepted!"
