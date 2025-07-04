import importlib
import json
import os
from configparser import ConfigParser, SectionProxy
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import toml
import yaml
from dotenv import load_dotenv

from pyechonext.security.crypts import PSPCAlgorithm


def dynamic_import(module: str):
    """Dynamic import with importlib

    Args:
        module (str): module name

    Returns:
        module: imported module
    """
    return importlib.import_module(str(module))


@dataclass(frozen=True)
class Settings:
    """
    This class describes settings.
    """

    BASE_DIR: str
    TEMPLATES_DIR: str
    SECRET_KEY: str = PSPCAlgorithm().crypt("SECRET-KEY")
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Echonext webapp"
    LOCALE: str = "DEFAULT"
    LOCALE_DIR: str = None
    STATIC_DIR: str = "static"


class SettingsConfigType(Enum):
    """
    This class describes a settings configuration type.
    """

    INI = "ini"
    DOTENV = "dotenv"
    PYMODULE = "pymodule"
    TOML = "toml"
    YAML = "yaml"
    JSON = "json"


class SettingsLoader:
    """
    This class describes a settings loader.
    """

    __slots__ = ("config", "config_type", "filename")

    def __init__(self, config_type: SettingsConfigType, filename: str = None):
        """Initialize a basic settings info

        Args:
            config_type (SettingsConfigType): file config type
            filename (str, optional): config filename. Defaults to None.

        Raises:
            FileNotFoundError: _description_
        """
        self.config = None
        self.config_type: SettingsConfigType = config_type
        self.filename: Path = Path(filename)

        if not self.filename.exists():
            raise FileNotFoundError(
                f'Config file "{self.filename}" don\'t exists.')

    def _load_yaml_config(self) -> dict:
        """Loads a config data from YAML file

        Returns:
            dict: config data
        """
        with open(self.filename, "r") as fh:
            data = yaml.load(fh, Loader=yaml.FullLoader)

        return data

    def _load_toml_config(self) -> dict:
        """Loads a config data from TOML file

        Returns:
            dict: config data
        """
        with open(self.filename, "r") as fh:
            data = toml.loads(fh)

        return data

    def _load_json_config(self) -> dict:
        """Loads a config data from JSON file

        Returns:
            dict: config data
        """
        with open(self.filename, "r") as fh:
            data = json.load(fh)

        return data

    def _load_ini_config(self) -> SectionProxy:
        """Loads a config data from INI file

        Returns:
            dict: config data
        """
        config = ConfigParser()
        config.read(self.filename)

        return config["Settings"]

    def _load_env_config(self) -> dict:
        """Loads a config data from ENV file

        Returns:
            dict: config data
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
            "STATIC_DIR": os.environ.get("PEN_STATIC_DIR", "static"),
        }

        return config

    def _load_pymodule_config(self) -> dict:
        """Loads configuration from python module

        Returns:
            dict: _description_
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
            "STATIC_DIR": config_module.STATIC_DIR,
        }

    def get_settings(self) -> Settings:
        """Get the settings dataclass

        Returns:
            Settings: settings object
        """
        if self.config_type == SettingsConfigType.INI:
            self.config = self._load_ini_config()
        elif self.config_type == SettingsConfigType.DOTENV:
            self.config = self._load_env_config()
        elif self.config_type == SettingsConfigType.PYMODULE:
            self.config = self._load_pymodule_config()
        elif self.config_type == SettingsConfigType.TOML:
            self.config = self._load_toml_config()
        elif self.config_type == SettingsConfigType.YAML:
            self.config = self._load_yaml_config()
        elif self.config_type == SettingsConfigType.JSON:
            self.config = self._load_json_config()

        return Settings(
            BASE_DIR=self.config.get("BASE_DIR", "."),
            TEMPLATES_DIR=self.config.get("TEMPLATES_DIR", "templates"),
            SECRET_KEY=self.config.get("SECRET_KEY", ""),
            LOCALE=self.config.get("LOCALE", "DEFAULT"),
            LOCALE_DIR=self.config.get("LOCALE_DIR", None),
            VERSION=self.config.get("VERSION", "1.0.0"),
            DESCRIPTION=self.config.get("DESCRIPTION", "EchoNext webapp"),
            STATIC_DIR=self.config.get("STATIC_DIR", "static"),
        )
