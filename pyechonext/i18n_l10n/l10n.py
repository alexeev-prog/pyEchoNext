import json
import os
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from loguru import logger
from pyechonext.utils.exceptions import LocalizationNotFound


class LocalizationInterface(ABC):
	"""
	This class describes a locale interface.
	"""

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

	@abstractmethod
	def format_date(self, date: datetime, date_format: Optional[str] = None) -> str:
		"""
		Format date

		:param		date:  The date
		:type		date:  datetime

		:returns:	formatted date
		:rtype:		str
		"""
		raise NotImplementedError

	@abstractmethod
	def format_number(self, number: float, decimal_places: int = 2) -> str:
		"""
		Format number

		:param		number:			 The number
		:type		number:			 float
		:param		decimal_places:	 The decimal places
		:type		decimal_places:	 int

		:returns:	formatted number
		:rtype:		str
		"""
		raise NotImplementedError

	@abstractmethod
	def format_currency(self, amount: float) -> str:
		"""
		Format currency

		:param		amount:	 The amount
		:type		amount:	 float

		:returns:	formatted currency
		:rtype:		str
		"""
		raise NotImplementedError

	@abstractmethod
	def get_current_settings(self) -> Dict[str, Any]:
		"""
		Gets the current settings.

		:returns:	The current settings.
		:rtype:		Dict[str, Any]
		"""
		raise NotImplementedError

	@abstractmethod
	def update_settings(self, settings: Dict[str, Any]):
		"""
		Update settings

		:param		settings:  The settings
		:type		settings:  Dict[str, Any]
		"""
		raise NotImplementedError


class JSONLocalizationLoader(LocalizationInterface):
	"""
	This class describes a json localization loader.
	"""

	DEFAULT_LOCALE = {
		"date_format": "%Y-%m-%d",
		"time_format": "%H:%M",
		"date_time_fromat": "%Y-%m-%d %H:%M",
		"thousands_separator": ",",
		"decimal_separator": ".",
		"currency_symbol": "$",
		"currency_format": "{symbol}{amount}",
	}

	def __init__(
		self,
		locale: str,
		directory: str,
		custom_settings: Optional[Dict[str, Any]] = None,
	):
		"""
		Constructs a new instance.

		:param		locale:			  The locale
		:type		locale:			  str
		:param		directory:		  The directory
		:type		directory:		  str
		:param		custom_settings:  The custom settings
		:type		custom_settings:  Optional[Dict[str, Any]]
		"""
		self.locale: str = locale
		self.directory: str = directory
		self.locale_settings: Dict[str, Any] = self.load_locale(locale, directory)

		if custom_settings:
			self.update_settings(custom_settings)

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
				l10n = json.load(file).get("l10n", None)
				if l10n is None:
					return json.load(file)
				else:
					return l10n
		except FileNotFoundError:
			raise LocalizationNotFound(f"[l10n] l10n file at {file_path} not found")

	def format_date(self, date: datetime, date_format: Optional[str] = None) -> str:
		"""
		Format date

		:param		date:		  The date
		:type		date:		  datetime
		:param		date_format:  The date format
		:type		date_format:  Optional[str]

		:returns:	formatted date
		:rtype:		str
		"""
		date_time_fromat = (
			self.locale_settings.get(
				"date_time_fromat", self.DEFAULT_LOCALE["date_time_fromat"]
			)
			if date_format is None
			else date_format
		)

		formatted_date = date_time_fromat.strftime(date_time_fromat)

		return formatted_date

	def format_number(self, number: float, decimal_places: int = 2) -> str:
		"""
		Format number

		:param		number:			 The number
		:type		number:			 float
		:param		decimal_places:	 The decimal places
		:type		decimal_places:	 int

		:returns:	formatted number
		:rtype:		str
		"""
		thousands_separator = self.locale_settings.get(
			"thousands_separator", self.DEFAULT_LOCALE["thousands_separator"]
		)
		decimal_separator = self.locale_settings.get(
			"decimal_separator", self.DEFAULT_LOCALE["decimal_separator"]
		)

		formatted_number = (
			f"{number:,.{decimal_places}f}".replace(",", "TEMP")
			.replace(".", decimal_separator)
			.replace("TEMP", thousands_separator)
		)
		return formatted_number

	def format_currency(self, amount: float) -> str:
		"""
		Format currency

		:param		amount:	 The amount
		:type		amount:	 float

		:returns:	formatted currency
		:rtype:		str
		"""
		currency_symbol = self.locale_settings.get(
			"currency_symbol", self.DEFAULT_LOCALE["currency_symbol"]
		)
		currency_format = self.locale_settings.get(
			"currency_format", self.DEFAULT_LOCALE["currency_format"]
		)

		return currency_format.format(
			symbol=currency_symbol, amount=self.format_number(amount)
		)

	def update_settings(self, settings: Dict[str, Any]):
		"""
		Update settings

		:param		settings:	 The settings
		:type		settings:	 Dict[str, Any]

		:raises		ValueError:	 setting is not recognized
		"""
		for key, value in settings.items():
			if key in self.locale_settings:
				self.locale_settings[key] = value
			elif key in self.DEFAULT_LOCALE:
				self.DEFAULT_LOCALE[key] = value
			else:
				raise ValueError(f'[l10n] Setting "{key}" is not recognized.')

	def get_current_settings(self) -> Dict[str, Any]:
		"""
		Gets the current settings.

		:returns:	The current settings.
		:rtype:		Dict[str, Any]
		"""
		return {
			"locale": self.locale,
			"directory": self.directory,
			**self.locale_settings,
			**self.DEFAULT_LOCALE,
		}
