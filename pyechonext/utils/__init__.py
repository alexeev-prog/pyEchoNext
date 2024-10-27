def _prepare_url(url: str) -> str:
	try:
		if url[-1] == "/":
			return url[:-1]
	except IndexError:
		return "/"

	return url
