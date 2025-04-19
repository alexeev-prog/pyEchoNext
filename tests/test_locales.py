from datetime import datetime

from pyechonext.i18n_l10n import JSONi18nLoader, JSONLocalizationLoader, LanguageManager

date = datetime.strptime("1980 01 01 00 00 00", "%Y %m %d %H %M %S").date()


def test_i18n():
    i18n_loader = JSONi18nLoader("DEFAULT")
    lm = LanguageManager(i18n_loader)

    assert lm.translate("Test: title") == "Test: pyEchoNext Example Website"


def test_l10n():
    l10n_loader = JSONLocalizationLoader("DEFAULT")
    assert l10n_loader.format_number(1000.0) == "1,000.00"
    assert l10n_loader.format_currency(3000.0) == "$3,000.00"
    assert l10n_loader.format_date(date) == "1980-01-01 00:00"
