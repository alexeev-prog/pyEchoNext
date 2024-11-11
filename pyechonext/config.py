import os
import importlib
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from configparser import ConfigParser
from dotenv import load_dotenv


def dynamic_import(module: str):
	"""
	Dynamic import with importlib

	:param		module:	 The module
	:type		module:	 str

	:returns:	module
	:rtype:		module
	"""
	return importlib.import_module(str(module))


@dataclass
class Settings:
	"""
	This class describes settings.
	"""

	BASE_DIR: str
	TEMPLATES_DIR: str
	SECRET_KEY: str
	VERSION: str = "1.0.0"
	DESCRIPTION: str = "Echonext webapp"
	LOCALE: str = "DEFAULT"
	LOCALE_DIR: str = None


class SettingsConfigType(Enum):
	"""
	This class describes a settings configuration type.
	"""

	INI = "ini"
	DOTENV = "dotenv"
	PYMODULE = "pymodule"


class SettingsLoader:
	"""
	This class describes a settings loader.
	"""

	def __init__(self, config_type: SettingsConfigType, filename: str = None):
		"""
		Constructs a new instance.

		:param		config_type:  The configuration type
		:type		config_type:  SettingsConfigType
		:param		filename:	  The filename
		:type		filename:	  str
		"""
		self.config_type: SettingsConfigType = config_type
		self.filename: str = filename

		self.filename: Path = Path(self.filename)

		if not self.filename.exists():
			raise FileNotFoundError(f'Config file "{self.filename}" don\'t exists.')

	def _load_ini_config(self) -> dict:
		"""
		Loads a .ini config file

		:returns:	config dictionary
		:rtype:		dict
		"""
		config = ConfigParser()
		config.read(self.filename)

		return config["Settings"]

	def _load_env_config(self) -> dict:
		"""
		Loads an environment configuration.

		:returns:	config dictionary
		:rtype:		dict
		"""
		load_dotenv(self.filename)

		config = {
			"BASE_DIR": os.environ.get("PEN_BASE_DIR"),
			"TEMPLATES_DIR": os.environ.get("PEN_TEMPLATES_DIR"),
			"SECRET_KEY": os.environ.get("PEN_SECRET_KEY"),
			"LOCALE": os.environ.get("PEN_LOCALE", "DEFAULT"),
			"LOCALE_DIR": os.environ.get("PEN_LOCALE_DIR", None),
			"VERSION": os.environ.get("PEN_VERSION", "1.0.0"),
			"DESCRIPTION": os.environ.get("PEN_DESCRIPTION", "EchoNext webapp"),
		}

		return config

	def _load_pymodule_config(self) -> dict:
		"""
		Loads a pymodule configuration.

		:returns:	config dictionary
		:rtype:		dict
		"""
		config_module = dynamic_import(str(self.filename).replace(".py", ""))

		return {
			"BASE_DIR": config_module.BASE_DIR,
			"TEMPLATES_DIR": config_module.TEMPLATES_DIR,
			"SECRET_KEY": config_module.SECRET_KEY,
			"LOCALE": config_module.LOCALE,
			"LOCALE_DIR": config_module.LOCALE_DIR,
			"VERSION": config_module.VERSION,
			"DESCRIPTION": config_module.DESCRIPTION,
		}

	def get_settings(self) -> Settings:
		"""
		Gets the settings.

		:returns:	The settings.
		:rtype:		Settings
		"""
		if self.config_type == SettingsConfigType.INI:
			self.config = self._load_ini_config()
		elif self.config_type == SettingsConfigType.DOTENV:
			self.config = self._load_env_config()
		elif self.config_type == SettingsConfigType.PYMODULE:
			self.config = self._load_pymodule_config()

		return Settings(
			BASE_DIR=self.config.get("BASE_DIR", "."),
			TEMPLATES_DIR=self.config.get("TEMPLATES_DIR", "templates"),
			SECRET_KEY=self.config.get("SECRET_KEY", ""),
			LOCALE=self.config.get("LOCALE", "DEFAULT"),
			LOCALE_DIR=self.config.get("LOCALE_DIR", None),
			VERSION=self.config.get("VERSION", "1.0.0"),
			DESCRIPTION=self.config.get("DESCRIPTION", "EchoNext webapp"),
		)
