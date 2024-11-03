from datetime import datetime


def get_current_datetime() -> str:
	"""
	Gets the current datetime.

	:returns:	The current datetime.
	:rtype:		str
	"""
	date = datetime.now()
	return date.strftime("%Y-%m-%d %H:%M:%S")


def _prepare_url(url: str) -> str:
	"""
	Prepare URL (remove ending /)

	:param		url:  The url
	:type		url:  str

	:returns:	prepared url
	:rtype:		str
	"""
	try:
		if url[-1] == "/" and len(url) > 1:
			return url[:-1]
	except IndexError:
		return "/"

	return url
