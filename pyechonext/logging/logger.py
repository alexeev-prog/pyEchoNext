import logging
from typing import Union, List
from loguru import logger


class InterceptHandler(logging.Handler):
	"""
	This class describes an intercept handler.
	"""

	def emit(self, record) -> None:
		"""
		Get corresponding Loguru level if it exists

		:param		record:	 The record
		:type		record:	 record

		:returns:	None
		:rtype:		None
		"""
		try:
			level = logger.level(record.levelname).name
		except ValueError:
			level = record.levelno

		frame, depth = logging.currentframe(), 2

		while frame.f_code.co_filename == logging.__file__:
			frame = frame.f_back
			depth += 1

		logger.opt(depth=depth, exception=record.exc_info).log(
			level, record.getMessage()
		)


def setup_logger(
	filename: str, level: Union[str, int] = "DEBUG", ignored: List[str] = ""
) -> None:
	"""
	Setup logger

	:param		level:	  The level
	:type		level:	  str
	:param		ignored:  The ignored
	:type		ignored:  List[str]
	"""
	logging.basicConfig(
		handlers=[InterceptHandler()], level=logging.getLevelName(level)
	)

	for ignore in ignored:
		logger.disable(ignore)

	logger.add(f"{filename}_app.log")

	logger.info("Logging is successfully configured")
