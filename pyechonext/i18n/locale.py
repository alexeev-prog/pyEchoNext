import json
import os
from abc import ABC, abstractmethod
from typing import Dict
from loguru import logger
from pyechonext.utils.exceptions import LocaleNotFound


class LocaleInterface(ABC):
	"""
	This class describes a locale interface.
	"""

	@abstractmethod
	def get_string(self, key: str) -> str:
		"""
		Gets the string.

		:param		key:  The key
		:type		key:  str

		:returns:	The string.
		:rtype:		str
		"""
		raise NotImplementedError


class JSONLocaleLoader(LocaleInterface):
	"""
	This class describes a json locale loader.
	"""

	DEFAULT_LOCALE = {
		"title": "pyEchoNext Example Website",
		"description": "This web application is an example of the pyEchonext web framework.",
	}

	def __init__(self, locale: str, directory: str):
		"""
		Constructs a new instance.

		:param		locale:		The locale
		:type		locale:		str
		:param		directory:	The directory
		:type		directory:	str
		"""
		self.locale = locale
		self.directory = directory
		self.translations: Dict[str, str] = self.load_locale(
			self.locale, self.directory
		)

	def load_locale(self, locale: str, directory: str) -> Dict[str, str]:
		"""
		Loads a locale.

		:param		locale:		The locale
		:type		locale:		str
		:param		directory:	The directory
		:type		directory:	str

		:returns:	locale dictionary
		:rtype:		Dict[str, str]
		"""
		if self.locale == "DEFAULT":
			return self.DEFAULT_LOCALE

		file_path = os.path.join(self.directory, f"{self.locale}.json")

		try:
			logger.info(f"Load locale: {file_path} [{self.locale}]")
			with open(file_path, "r", encoding="utf-8") as file:
				return json.load(file)
		except FileNotFoundError:
			raise LocaleNotFound(f"[i18n] Locale file at {file_path} not found")

	def get_string(self, key: str) -> str:
		"""
		Gets the string.

		:param		key:  The key
		:type		key:  str

		:returns:	The string.
		:rtype:		str
		"""
		return self.translations.get(key, key)


class LanguageManager:
	"""
	This class describes a language manager.
	"""

	def __init__(self, loader: LocaleInterface):
		"""
		Constructs a new instance.

		:param		loader:	 The loader
		:type		loader:	 LocaleInterface
		"""
		self.loader = loader

	def translate(self, key: str) -> str:
		"""
		Translate

		:param		key:  The key
		:type		key:  str

		:returns:	translated string
		:rtype:		str
		"""
		return self.loader.get_string(key)
