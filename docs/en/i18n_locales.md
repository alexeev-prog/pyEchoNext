# pyEchoNext / i18n - localization

---

pyEchoNext since version 0.5.3 supports i18n (so far in its basic form).

i18n is an abbreviation for internationalization process.

Internationalization is the process of developing an application in which its code is independent of any linguistic and cultural characteristics of the region or country. As a result, the application becomes flexible and can easily adapt to different language and cultural settings.

Internationalization implementation usually begins in the early stages of a project to prepare the product for future localization. During this process, they determine what will change for future locales (for example, text, images) and export this data to external files.

The 18 in i18n stands for the number of letters between the first letter i and the last letter n in the word "internationalization".

In pyEchoNext this is implemented like this: a Response is created, if you need to use i18n for localization, use the use_i18n flag:

```python
from pyechonext.response import Request, Response

# create a request...
# request = ...

response = Response(request, body='title', use_i18n=True)
```

This will signal to the application that i18n should be used in this Response. And the application will translate your phrase.

## Creating localizations
You pass the required Settings parameter to the application. It has two fields related to localization:

+ `LOCALE: str = "DEFAULT"`
+ `LOCALE_DIR: str = None`

By default they create the default locale. It looks like this:

```python
DEFAULT_LOCALE = {
"title": "pyEchoNext Example Website",
"description": "This web application is an example of the pyEchonext web framework.",
}
```

That is, if we enter only title or only description in response.body, we will end up with the phrase “pyEchoNext Example Website” or “This web application is an example of the pyEchoNext web framework.”.

But how to create your own locales? It's simple. Create a directory with locale files, we recommend locales, and localization json files in it. Let's say RU_RU.json:

```json
{
"title": "pyEchoNext Web application with locale",
"example one": "example one"
}
```

And already in Settings we specify the following settings:

+ `LOCAL = "RU_RU"`
+ `LOCALE_DIR = "locales"`

Or through the settings loader (in this example, through the python module, you can see [how to use the settings loader](./webapp_creation.md)):

```python
from pyechonext.config import SettingsLoader, SettingsConfigType

config_loader = SettingsLoader(SettingsConfigType.PYMODULE, 'el_config.py')
settings = config_loader.get_settings()
echonext = EchoNext(
__name__,
settings,
middlewares,
urls=url_patterns,
application_type=ApplicationType.HTML,
)
```

el_config.py:

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = 'templates'
SECRET_KEY = 'secret-key'
LOCAL = 'RU_RU'
LOCALE_DIR = 'locales'
```

The LOCALE value must be the same as the file name. If RU_RU, then the file should be RU_RU.json.

And now you can introduce internationalization to your application!

> At the time of version 0.5.3 i18n is under development, many features will be added later. The plans include: dividing the site localization into several files, more convenient handling of i18n and the ability to change localization on the fly. We plan to be inspired by [this documentation](https://developer.mozilla.org/ru/docs/Mozilla/Add-ons/WebExtensions/Internationalization), reworking it for our web framework.

---

[Contents](./index.md)
