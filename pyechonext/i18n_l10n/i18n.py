import json
import os
from abc import ABC, abstractmethod
from typing import Dict
from loguru import logger
from pyechonext.utils.exceptions import InternationalizationNotFound


class i18nInterface(ABC):
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

	@abstractmethod
	def load_locale(self, locale: str, directory: str) -> Dict[str, str]:
		"""
		Loads a locale.

		:param		locale:		The locale
		:type		locale:		str
		:param		directory:	The directory
		:type		directory:	str

		:returns:	locale translations
		:rtype:		Dict[str, str]
		"""
		raise NotImplementedError


class JSONi18nLoader(i18nInterface):
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
		self.locale: str = locale
		self.directory: str = directory
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
				i18n = json.load(file).get("i18n", None)
				if i18n is None:
					return json.load(file)
				else:
					return i18n
		except FileNotFoundError:
			raise InternationalizationNotFound(
				f"[i18n] i18n file at {file_path} not found"
			)

	def get_string(self, key: str, **kwargs) -> str:
		"""
		Gets the string.

		:param		key:	 The key
		:type		key:	 str
		:param		kwargs:	 The keywords arguments
		:type		kwargs:	 dictionary

		:returns:	The string.
		:rtype:		str
		"""
		result = ""

		for word in key.split(" "):
			result += f"{self.translations.get(word, word)} "

		if kwargs:
			for name, value in kwargs.items():
				result = result.replace(f'{f"%{{{name}}}"}', str(value))

		return result.strip()


class LanguageManager:
	"""
	This class describes a language manager.
	"""

	def __init__(self, loader: i18nInterface):
		"""
		Constructs a new instance.

		:param		loader:	 The loader
		:type		loader:	 i18nInterface
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
