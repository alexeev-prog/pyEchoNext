# pyEchoNext / i18n - локализация

---

pyEchoNext с версии 0.5.3 поддерживает i18n (пока в базовом виде).

i18n — это сокращённое обозначение процесса интернационализации.

Интернационализация — это процесс разработки приложения, при котором его код независим от любых языковых и культурных особенностей региона или страны. В результате приложение становится гибким и может легко адаптироваться под разные языковые и культурные настройки.

Реализацию интернационализации обычно начинают на ранних этапах проекта, чтобы подготовить продукт к будущей локализации. Во время этого процесса определяют, что будет изменяться для будущих локалей (например, текст, изображения) и выносят эти данные во внешние файлы.

18 в аббревиатуре i18n означает количество букв между первой буквой i и последней буквой n в слове «internationalization».

В pyEchoNext это реализовано так: создается Response, если нужно использовать i18n для локализации, используем флаг use_i18n: 

```python
from pyechonext.response import Request, Response

# создаем request ...
# request = ...

# ваш view или route
	response = Response(request, body='title', use_i18n=True)
```

Это будет сигнализировать приложению о том, что в данном Response следует использовать i18n. И приложение будет переводить вашу фразу.

Также вы можете и не возвращать response:

```python
return echonext.locale_loader.get_string('title')
```

В echonext есть публичный объект locale_loader, он и является загрузчиком локализации. Метод get_string получает строку из словаря локализации. Как их создавать и читать вы можете увидеть в секции "Создание локализаций" под этой.

Также вы можете использовать форматирование через Response:

```python
return Response(request, body="title %{name}", use_i18n=True, name='Localization site')
```

 > ЗАПРЕЩЕНЫ следующие аргументы (они заняты): `request: Request, use_i18n: bool = False, status_code: Optional[int] = 200, body: Optional[str] = None, headers: Optional[Dict[str, str]] = {}, content_type: Optional[str] = None, charset: Optional[str] = None, **kwargs`

Но для локализации мы рекомендуем возвращать контент, а не Response, особенно если вам требуется использовать наименования выше.

И вы можете как раз использовать форматирование напрямую:

```python
return echonext.locale_loader.get_string('title %{name}', name='Localization Site')
``` 

## Создание локализаций
В приложение вы передаете обязательный параметр Settings. В нем есть два поля относящиеся к локализации:

 + `LOCALE: str = "DEFAULT"`
 + `LOCALE_DIR: str = None`

По умолчанию они создают дефолтную локаль. Она выглядит так:

```python
DEFAULT_LOCALE = {
	"title": "pyEchoNext Example Website",
	"description": "This web application is an example of the pyEchonext web framework.",
}
```

То есть, если мы в response.body введем только title или только description, мы получим в итоге фразу "pyEchoNext Example Website" или "This web application is an example of the pyEchonext web framework.".

Но как создать свои локали? Все просто. Создайте директорию с файлами локалей, мы рекомендуем locales, и в ней json-файлы локализации. Допустим RU_RU.json:

```json
{
	"title": "pyEchoNext Веб-приложение с локалью",
	"example one": "пример один"
}
```

И уже в Settings мы указываем следующие настройки:

 + `LOCALE = "RU_RU"`
 + `LOCALE_DIR = "locales"`

Или через загрузчик настроек (в данном примере через python-модуль, вы можете посмотреть [как использовать загрузчик настроек](./webapp_creation.md)):

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
LOCALE = 'RU_RU'
LOCALE_DIR = 'locales'
```

Значение LOCALE должно совпадать с именем файла. Если RU_RU, то файл должен быть RU_RU.json.

И теперь вы можете вводить интернационализацию вашего приложения!

 > На момент версии 0.5.3 i18n находится в разработке, множество функционала будет добавлено позже. В планах: разделение локализации сайта на несколько файлов, более удобное обращение с i18n и возможность сменять локализацию "на лету". Мы планируем вдохновляться [этой документацией](https://developer.mozilla.org/ru/docs/Mozilla/Add-ons/WebExtensions/Internationalization), переработов ее для нашего веб-фреймворка.

---

[Содержание](./index.md)
