import os
import mimetypes
from pathlib import Path
from typing import List
from loguru import logger
from pyechonext.config import Settings
from pyechonext.utils.exceptions import StaticFileNotFoundError


class StaticFile:
	"""
	This class describes a static file.
	"""

	def __init__(self, settings: Settings, filename: str):
		"""
		Constructs a new instance.

		:param		settings:  The settings
		:type		settings:  Settings
		:param		filename:  The filename
		:type		filename:  str
		"""
		self.settings = settings
		self.filename = f"/{settings.STATIC_DIR}/{filename}".replace("//", "/")
		self.abs_filename = Path(
			os.path.join(self.settings.BASE_DIR, self.settings.STATIC_DIR, filename)
		)

		if not self.abs_filename.exists():
			raise StaticFileNotFoundError(
				f'Static file "{self.abs_filename}" not found.'
			)

	def load_content(self) -> str:
		"""
		Loads a content.

		:returns:	static file content
		:rtype:		str
		"""
		with open(self.abs_filename, "r") as file:
			return file.read().strip()

	def get_content_type(self) -> str:
		"""
		Gets the content type.

		:returns:	The content type.
		:rtype:		str
		"""
		content_type, _ = mimetypes.guess_type(str(self.abs_filename))

		return content_type or "application/octet-stream"

	def get_file_size(self) -> int:
		"""
		Gets the file size.

		:returns:	The file size.
		:rtype:		int
		"""
		return self.abs_filename.stat().st_size


class StaticFilesManager:
	"""
	This class describes a static files manager.
	"""

	def __init__(self, static_files: List[StaticFile]):
		"""
		Constructs a new instance.

		:param		static_files:  The static files
		:type		static_files:  List[StaticFile]
		"""
		self.static_files = static_files

	def get_file_type(self, url: str) -> str:
		"""
		Gets the file type.

		:param		url:  The url
		:type		url:  str

		:returns:	The file type.
		:rtype:		str
		"""
		for static_file in self.static_files:
			if static_file.filename == url:
				return static_file.get_content_type()

	def get_file_size(self, url: str) -> str:
		"""
		Gets the file size.

		:param		url:  The url
		:type		url:  str

		:returns:	The file size.
		:rtype:		str
		"""
		for static_file in self.static_files:
			if static_file.filename == url:
				return static_file.get_file_size()

	def serve_static_file(self, url: str) -> str:
		"""
		Server static file by url

		:param		url:  The url
		:type		url:  str

		:returns:	static file content
		:rtype:		str
		"""
		for static_file in self.static_files:
			if static_file.filename == url:
				logger.info(f"Found static file: {static_file.filename}")
				return static_file.load_content()

		logger.warning(f'Static file "{url}" not found.')
		return False
