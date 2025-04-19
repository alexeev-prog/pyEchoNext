from pyechonext.config import SettingsConfigType, SettingsLoader


def test_config():
    config_loader = SettingsLoader(SettingsConfigType.PYMODULE, "config.py")
    settings = config_loader.get_settings()

    assert settings.TEMPLATES_DIR == "templates"
    assert settings.SECRET_KEY == "secret-key"
    assert settings.LOCALE == "RU_RU"
    assert settings.LOCALE_DIR == "locales"
    assert settings.VERSION == "0.1.0"
    assert settings.DESCRIPTION == "Example echonext webapp"
    assert settings.STATIC_DIR == "static"


def test_env():
    config_loader = SettingsLoader(SettingsConfigType.DOTENV, "example_env")
    settings = config_loader.get_settings()

    assert settings.TEMPLATES_DIR == "templates"
    assert settings.SECRET_KEY == "secret-key"
    assert settings.LOCALE == "RU_RU"
    assert settings.LOCALE_DIR == "locales"
    assert settings.VERSION == "0.1.0"
    assert settings.DESCRIPTION == "Example"
    assert settings.STATIC_DIR == "static"


def test_ini():
    config_loader = SettingsLoader(SettingsConfigType.INI, "example_ini.ini")
    settings = config_loader.get_settings()

    assert settings.TEMPLATES_DIR == "templates"
    assert settings.SECRET_KEY == "secret-key"
    assert settings.LOCALE == "RU_RU"
    assert settings.LOCALE_DIR == "locales"
    assert settings.VERSION == "0.1.0"
    assert settings.DESCRIPTION == "Example"
    assert settings.STATIC_DIR == "static"
