from loguru import logger


class pyEchoNextException(Exception):
	"""
	Exception for signaling pyechonext errors.
	"""

	def __init__(self, *args):
		"""
		Constructs a new instance.

		:param		args:  The arguments
		:type		args:  list
		"""
		if args:
			self.message = args[0]
		else:
			self.message = None

	def get_explanation(self) -> str:
		"""
		Gets the explanation.

		:returns:	The explanation.
		:rtype:		str
		"""
		return f"Message: {self.message if self.message else 'missing'}"

	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"pyEchoNextException has been raised. {self.get_explanation()}"


class WebError(pyEchoNextException):
	code = 400

	def get_explanation(self) -> str:
		"""
		Gets the explanation.

		:returns:	The explanation.
		:rtype:		str
		"""
		return (
			f"Code: {self.code}. Message: {self.message if self.message else 'missing'}"
		)

	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"WebError has been raised. {self.get_explanation()}"


class TemplateNotFileError(pyEchoNextException):
	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"TemplateNotFileError has been raised. {self.get_explanation()}"


class RoutePathExistsError(pyEchoNextException):
	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"RoutePathExistsError has been raised. {self.get_explanation()}"


class URLNotFound(WebError):
	code = 404

	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"URLNotFound has been raised. {self.get_explanation()}"


class MethodNotAllow(WebError):
	code = 405

	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"MethodNotAllow has been raised. {self.get_explanation()}"
