# Как создать свой веб-фреймворк на Python
Доброго времени суток, хабр! В этой статье мы создадим свой веб-фреймворк на Python с использованием gunicorn.

Он будет легким, иметь базовый функционал. Мы создадим обработчики запросов (views), простую и параметизированную маршрутизацию, Middleware, i18n и l10n, Request/Response, обработку html-шаблонов и генерацию документации.

В этой статьи мы построим наиболее важные части фреймворка, изучим работу WSGI и создание веб-приложений. И также нам будет легче в последующем понимать логику других фреймворков: flask, django.

Некоторые из вас могут сказать что мы изобретаем велосипед. А я в ответ скажу - сможете ли вы прямо сейчас, без подсказок, только по памяти, нарисовать велосипед без ошибок?

---

Наиболее важными частями веб-фрейморков являются:

 + Обработчики маршрутизации (routes):
   - Простые: `/index`
   - Параметризованные: `/article/{article_id}`
 + Обработчики запросов (views).
 + Middleware
 + Request/Response
 + i18n/l10n
 + Конфигурация

Основное требование: веб-фреймворк должен поддерживаться быстрым, легким и эффективным сервером (например gunicorn). Для этого в Python есть руководство по WSGI.

Наш веб-фреймворк будет называться pyEchoNext. [Ссылка на репозиторий.](https://github.com/alexeev-prog/pyEchoNext)

# Устройство веб-сервера на Python

```
            ЗАПРОС
CLIENT <--------------> [HTTP (80) или HTTPS (443)] Сервер
             ОТВЕТ
   
        > Приложение с логикой
        > Преобразование данных для python-приложения  <-- Зона интересов веб-фреймвока (обеспечение работы gunicorn с ним)
        > Gunicorn
        > Преобразованные данные
СЕРВЕР -> NGINX
        > Маршрутизация данных
```

При разработки web-приложения на python мы сталкиваемся со следующими проблемами:

 + Многие фреймворки (ex. django) не умеют маршрутизировать ответные запросы.
 + Приложения являются небезопасными, и могут быть подвержены DDoS-атаке (Distributed Denial of Service, распределенный отказ в обслуживании).
 + Нет балансировки нагрузки между несколькими серверами.
 + Проблему балансировки нагрузки решает NGINX, но он не умеет запускать и общаться с Python-приложениями.

Поэтому и возникает нужда в использовании WSGI-сервера (Web Server Gateway Interface) и прокси-сервера (такого как NGINX).

# WSGI
В настоящее время Python может похвастаться широким спектром фреймворков веб-приложений, таких как Zope, Quixote, Webware, SkunkWeb, PSO и Twisted Web — вот лишь некоторые из них. Такое широкое разнообразие вариантов может стать проблемой для новых пользователей Python, поскольку, как правило, их выбор веб-фреймворка ограничит их выбор используемых веб-серверов, и наоборот.

Напротив, хотя Java имеет столько же доступных фреймворков веб-приложений, API «servlet» Java позволяет приложениям, написанным с помощью любого фреймворка веб-приложений Java, работать на любом веб-сервере, который поддерживает API сервлетов.

Доступность и широкое использование такого API в веб-серверах для Python — независимо от того, написаны ли эти серверы на Python (например, Medusa), встроен ли Python (например, mod_python) или вызывают Python через протокол шлюза (например, CGI, FastCGI и т. д.) — отделит выбор фреймворка от выбора веб-сервера, позволяя пользователям выбирать подходящую им пару, в то же время освобождая разработчиков фреймворка и сервера для сосредоточения на их предпочтительной области специализации.

Таким образом, этот PEP предлагает простой и универсальный интерфейс между веб-серверами и веб-приложениями или фреймворками: интерфейс шлюза веб-сервера Python (WSGI).

Но само существование спецификации WSGI ничего не делает для решения существующего состояния серверов и фреймворков для веб-приложений Python. Авторы и сопровождающие серверов и фреймворков должны фактически реализовать WSGI, чтобы это имело какой-либо эффект.

Однако, поскольку ни один из существующих серверов или фреймворков не поддерживает WSGI, автор, который реализует поддержку WSGI, не получит немедленного вознаграждения.Таким образом, WSGI должен быть прост в реализации, чтобы первоначальные инвестиции автора в интерфейс могли быть достаточно низкими.

Таким образом, простота реализации как на стороне сервера, так и на стороне фреймворка интерфейса абсолютно критична для полезности интерфейса WSGI и, следовательно, является основным критерием для любых проектных решений.

Однако следует отметить, что простота реализации для автора фреймворка — это не то же самое, что простота использования для автора веб-приложения. WSGI представляет абсолютно «без излишеств» интерфейс для автора фреймворка, потому что такие навороты, как объекты ответа и обработка файлов cookie, просто помешают существующим фреймворкам решать эти проблемы. Опять же, цель WSGI — облегчить простое взаимодействие существующих серверов и приложений или фреймворков, а не создать новый веб-фреймворк.

Также следует отметить, что эта цель не позволяет WSGI требовать ничего, что еще не доступно в развернутых версиях Python. Поэтому новые модули стандартной библиотеки не предлагаются и не требуются этой спецификацией, и ничто в WSGI не требует версии Python выше 2.2.2. (Однако было бы неплохо, чтобы будущие версии Python включали поддержку этого интерфейса в веб-серверах, предоставляемых стандартной библиотекой.)

Помимо простоты реализации для существующих и будущих фреймворков и серверов, также должно быть легко создавать препроцессоры запросов, постпроцессоры ответов и другие компоненты «промежуточного программного обеспечения» на основе WSGI, которые выглядят как приложение для своего содержащего сервера, при этом выступая в качестве сервера для своих содержащихся приложений.Если промежуточное ПО может быть одновременно простым и надежным, а WSGI широко доступен в серверах и фреймворках, это допускает возможность совершенно нового типа фреймворка веб-приложений Python: состоящего из слабосвязанных компонентов промежуточного ПО WSGI. Действительно, существующие авторы фреймворков могут даже выбрать рефакторинг существующих служб своих фреймворков, чтобы они предоставлялись таким образом, становясь больше похожими на библиотеки, используемые с WSGI, и меньше на монолитные фреймворки. Это тогда позволило бы разработчикам приложений выбирать «лучшие в своем классе» компоненты для определенной функциональности, вместо того, чтобы брать на себя все плюсы и минусы одного фреймворка.

Конечно, на момент написания этой статьи этот день, несомненно, довольно далек. В то же время, это является достаточной краткосрочной целью для WSGI, чтобы обеспечить использование любого фреймворка с любым сервером.

Наконец, следует упомянуть, что текущая версия WSGI не предписывает какой-либо конкретный механизм для «развертывания» приложения для использования с веб-сервером или серверным шлюзом. В настоящее время это обязательно определяется реализацией сервера или шлюза. После того, как достаточное количество серверов и фреймворков внедрит WSGI для обеспечения практического опыта с различными требованиями к развертыванию, может иметь смысл создать еще один PEP, описывающий

# Цели pyEchoNext
pyEchoNext - универсальный инструмент с возможностью сделать монолитное веб-приложение, или наоборот, модульное веб-приложение. Django для нас был слишком большой и неповоротливый, flask или fastapi слишком маленький. Поэтому мы решили взять некоторые фичи из django и flask/fastapi, соединить их и сделать так чтобы все это было в симбиозе. Так, чтобы можно было и сделать большой монолитный проект, так и маленький сервис. И чтобы превратить маленький сервис в большое приложение или наоборот требовалось минимум усилий.

Также нашими целями было сделать все это максимально понятным, дружественным к разработчику и добавить возможности интеграции сторонних библиотек.

В итоге, основная характеристика проекта такая:

1. Цель: Создать универсальный многогранный веб-фреймворк на python

2. Задачи:

 + Найти хорошие и плохие стороны Flask, FastAPI
 + Найти хорошие и плохие стороны Django
 + Сравнить возможности существующих фреймворков
 + Выбор лучших фич
 + Симбиоз фич в одно целое
 + Построить код проекта согласно SOLID и принципам ООП, легко расширяемым, масштабируемым и дополняемым.
 + Сделать код быстрым и производительным, дать свободу пользователю и разработчику

3. Проблема: на данный момент очень мало универсальных фреймворков, дающих создать как и большое монолитное приложение, так и быстрый маленький сервис.

4. Актуальность: веб-сфера в данное время очень сильно популярна, умение работать с веб-фреймворками, абстракциями, знать устройство сайтов поможет всем.

# Как работает запуск веб-приложения через gunicorn
Установите `gunicorn` и `pysocks` для последующих действий.

Итак, создайте файл app.py:

```python
from socks import method


def app(environ: dict, start_response: method):
	response_body = b'Hello, Habr!'
	status = "200 OK"
	start_response(status, headers=[])
	return iter([response_body])
```

И после запустите gunicorn:

```bash
gunicorn app:app
# gunicorn <файл>:<callable-класс или функция точки входа>
```

Точка входа получает два параметра - environ и start_response. В environ содержится вся информация о веб-окружении, такие как user-agent, путь, метод, GET и POST параметры и другие. Второй параметр - start_response, стартовый ответ, который высылает предпологаемый ответ.

Но более хорошой практикой будет создать callable-класс:

```python
class App:
	def __call__(self, environ: dict, start_response: method):
		response_body = b'Hello, Habr!'
		status = "200 OK"
		start_response(status, headers=[])
		return iter([response_body])


app = App()
```

Магический метод `__call__` делает объекты нашего класса вызываемыми.

И теперь вы абсолютно также можете запустить приложение:

```bash
gunicorn app:app
# gunicorn <файл>:<callable-класс или функция точки входа>
```

Но давайте теперь постепенно заполнять наш проект, наполняя его различными модулями. Давайте начнем с создания проекта через poetry.

# Создание проекта

Poetry — это инструмент для управления зависимостями и сборкой пакетов в Python. А также при помощи Poetry очень легко опубликовать свою библиотеку на PyPi!

В Poetry представлен полный набор инструментов, которые могут понадобиться для детерминированного управления проектами на Python. В том числе, сборка пакетов, поддержка разных версий языка, тестирование и развертывание проектов.

Все началось с того, что создателю Poetry Себастьену Юстасу потребовался единый инструмент для управления проектами от начала до конца, надежный и интуитивно понятный, который бы мог использоваться и в рамках сообщества. Одного лишь менеджера зависимостей было недостаточно, чтобы управлять запуском тестов, процессом развертывания и всем созависимым окружением. Этот функционал находится за гранью возможностей обычных пакетных менеджеров, таких как Pip или Conda. Так появился Python Poetry.

Установить poetry можно через pipx: `pipx install poetry` и через pip: `pip install poetry --break-system-requirements`. Это установит poetry глобально во всю систему.

Итак, давайте создадим проект при помощи poetry и установим зависимости:

```bash
poetry new <имя_проекта>
cd <имя_проекта>
poetry shell
poetry add ruff loguru pysocks fire python-dotenv jinja2 parse gunicorn configparser
```

## Архитектура проекта
У меня получилась следующая архитектура проекта:

```
pyechonext/
├── apidoc_ui
│   ├── api_documentation.py
│   └── __init__.py
├── app.py
├── config.py
├── docsgen
│   ├── document.py
│   ├── __init__.py
│   └── projgen.py
├── i18n_l10n
│   ├── i18n.py
│   └── l10n.py
├── __init__.py
├── logging
│   ├── __init__.py
│   └── logger.py
├── __main__.py
├── middleware.py
├── request.py
├── response.py
├── template_engine
│   ├── builtin.py
│   ├── __init__.py
│   └── jinja.py
├── urls.py
├── utils
│   ├── exceptions.py
│   └── __init__.py
└── views.py
```

 + Директория apidoc_ui - это генерация OpenAPI документации проекта.
 + Директория docsgen - генерация документации проекта
 + Директория i18n_l10n - интернационализация и локализация
 + Директория logging - логгирование
 + Директория template_engine - движки html-шаблонов
 + Директория utils - утилиты
 + Файл app.py - приложение
 + Файл config.py - конфигурация и загрузка настроек
 + Файл `__main__.py` - главный модуль, для запуска через `python3 -m pyechonext`
 + Файл middleware.py - промежуточное ПО
 + Файл request.py - класс запроса
 + Файл response.py - класс ответа
 + Файл urls.py - URL (обработчики)
 + Файл views.py - обработчики запросов

# Реализуем кастомные исключения
Исключения - неотъемлимая часть веб-фреймворка. Я решил реализовать несколько родительских классов:

 + pyEchoNextException - базовое исключение
 + WebError - веб-ошибка (наследуется от pyEchoNextException). Отличается тем, что имеет HTTP-код ошибки.

Поэтому имеются следующие исключения-наследники pyEchoNextException:

 + InternationalizationNotFound - файл интернационализации не найден
 + LocalizationNotFound - файл локализации не найден
 + TemplateNotFileError - шаблон не является файлом
 + RoutePathExistsError - путь маршрута уже существует

И следующие исключения-наследники WebError:

 + URLNotFound - URL не найден (404)
 + MethodNotAllow - метод не разрешается (405)
 + TeapotError - сервер является чайником (418)

<details>
	<summary>Исходный код кастомных исключений</summary>

```python
from loguru import logger


class pyEchoNextException(Exception):
	"""
	Exception for signaling pyechonext errors.
	"""

	def __init__(self, *args):
		"""
		Constructs a new instance.

		:param		args:  The arguments
		:type		args:  list
		"""
		if args:
			self.message = args[0]
		else:
			self.message = None

	def get_explanation(self) -> str:
		"""
		Gets the explanation.

		:returns:	The explanation.
		:rtype:		str
		"""
		return f"Message: {self.message if self.message else 'missing'}"

	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"pyEchoNextException has been raised. {self.get_explanation()}"


class WebError(pyEchoNextException):
	code = 400

	def get_explanation(self) -> str:
		"""
		Gets the explanation.

		:returns:	The explanation.
		:rtype:		str
		"""
		return (
			f"Code: {self.code}. Message: {self.message if self.message else 'missing'}"
		)

	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"WebError has been raised. {self.get_explanation()}"


class InternationalizationNotFound(pyEchoNextException):
	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"InternationalizationNotFound has been raised. {self.get_explanation()}"


class LocalizationNotFound(pyEchoNextException):
	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"LocalizationNotFound has been raised. {self.get_explanation()}"


class TemplateNotFileError(pyEchoNextException):
	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"TemplateNotFileError has been raised. {self.get_explanation()}"


class RoutePathExistsError(pyEchoNextException):
	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"RoutePathExistsError has been raised. {self.get_explanation()}"


class URLNotFound(WebError):
	code = 404

	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"URLNotFound has been raised. {self.get_explanation()}"


class MethodNotAllow(WebError):
	code = 405

	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"MethodNotAllow has been raised. {self.get_explanation()}"


class TeapotError(WebError):
	code = 418

	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		logger.error(f"{self.__class__.__name__}: {self.get_explanation()}")
		return f"The server refuses to make coffee because he is a teapot. {self.get_explanation()}"
```
</details>

# Реализуем интернационализацию и локализацию
i18n — это сокращённое обозначение процесса интернационализации.
l10n - локализация, то есть процесс учитывания культуры и правила написания дат, денежных сумм, чисел.

Интернационализация — это процесс разработки приложения, при котором его код независим от любых языковых и культурных особенностей региона или страны. В результате приложение становится гибким и может легко адаптироваться под разные языковые и культурные настройки.

Реализацию интернационализации обычно начинают на ранних этапах проекта, чтобы подготовить продукт к будущей локализации. Во время этого процесса определяют, что будет изменяться для будущих локалей (например, текст, изображения) и выносят эти данные во внешние файлы.

18 в аббревиатуре i18n означает количество букв между первой буквой i и последней буквой n в слове «internationalization».

В нашем проекте в файле i18n.py будет два класса - абстрактный i18nInterface. Он имеет два абстрактных метода - load_locale и get_string.

От него наследуется класс JSONi18nLoader, он загружает интернационализацию из json-файла. Но у него есть локализация по умолчанию:

```python
DEFAULT_LOCALE = {
	"title": "pyEchoNext Example Website",
	"description": "This web application is an example of the pyEchonext web framework.",
}
```

json-файл должен иметь такое название: `<локаль>.json`. Например, для RU_RU: `RU_RU.json`. И имеет следующий вид:

```json
{
	"i18n": {
		"title": "pyEchoNext Веб-приложение с локалью",
		"example one": "пример один"
	},
	"l10n": {
		"date_format": "%Y-%m-%d",
		"time_format": "%H:%M",
		"date_time_fromat": "%Y-%m-%d %H:%M",
		"thousands_separator": ",",
		"decimal_separator": ".",
		"currency_symbol": "$",
		"currency_format": "{symbol}{amount}"
	}
}
```

Как вы видите, в одном json-файле содержится и i18n, и l10n.

Такая же структура и у файла l10n.py - абстрактный класс LocalizationInterface с абстрактными методами load_locale, format_date, format_number, format_currency, get_current_settings и update_settings.

И абсолютно также имеется класс JSONLocalizationLoader (наследуется от интерфейса). Он уже имеет следующие дефолтные параметры:

```python
DEFAULT_LOCALE = {
	"date_format": "%Y-%m-%d",
	"time_format": "%H:%M",
	"date_time_fromat": "%Y-%m-%d %H:%M",
	"thousands_separator": ",",
	"decimal_separator": ".",
	"currency_symbol": "$",
	"currency_format": "{symbol}{amount}",
}
```

Эти параметры должны быть обязательны в файле локали, иначе несуществующий параметр заменится на дефолтный.

<details>
	<summary>Исходный код i18n.py</summary>

```python
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
				result = result.replace(f'{f"%{{{name}}}"}', value)

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
```
</details>

<details>
	<summary>Исходный код l10n.py</summary>

```python
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
```
</details>

# Реализуем логгирование
Мы до сих пор импортировали `from logger import loguru`, но я не объяснил что это. Loguru - это более удобная альтернатива-обертка вокруг logging. Для ее настройки создадим файл logging/logger.py:

```python
import logging
from typing import Union, List
from loguru import logger


class InterceptHandler(logging.Handler):
	"""
	This class describes an intercept handler.
	"""

	def emit(self, record) -> None:
		"""
		Get corresponding Loguru level if it exists

		:param		record:	 The record
		:type		record:	 record

		:returns:	None
		:rtype:		None
		"""
		try:
			level = logger.level(record.levelname).name
		except ValueError:
			level = record.levelno

		frame, depth = logging.currentframe(), 2

		while frame.f_code.co_filename == logging.__file__:
			frame = frame.f_back
			depth += 1

		logger.opt(depth=depth, exception=record.exc_info).log(
			level, record.getMessage()
		)


def setup_logger(level: Union[str, int] = "DEBUG", ignored: List[str] = "") -> None:
	"""
	Setup logger

	:param		level:	  The level
	:type		level:	  str
	:param		ignored:  The ignored
	:type		ignored:  List[str]
	"""
	logging.basicConfig(
		handlers=[InterceptHandler()], level=logging.getLevelName(level)
	)

	for ignore in ignored:
		logger.disable(ignore)

	logger.add("pyechonext.log")

	logger.info("Logging is successfully configured")
```

В коде выше мы назначаем файл лога, настраиваем его.

# Генерация документации проекта
Небольшой привет из моей прошлой статьи про управление документацией проекта при помощи python.

Я не буду описывать весь код, вы можете увидеть и интегрировать его к себе в проект из [моей статьи](https://habr.com/ru/companies/timeweb/articles/848584).

Но я добавил один файл - docsgen/projgen.py, он отвечает за генерацию:

```python
from typing import Callable, Any
from pyechonext.app import EchoNext
from pyechonext.docsgen.document import (
	InitiationSection,
	DocumentFolder,
	ProjectManager,
	ProjectTemplate,
	RoutesSubsection,
	DocumentSection,
)


class ProjDocumentation:
	"""
	This class describes an api documentation.
	"""

	def __init__(self, echonext_app: EchoNext):
		"""
		Constructs a new instance.

		:param		echonext_app:  The echonext application
		:type		echonext_app:  EchoNext
		"""
		self.app = echonext_app
		self.app_name = echonext_app.app_name
		self.pages = {}

	def generate_documentation(self):
		"""
		Generate documentation
		"""
		section = self._generate_introduction()
		self._generate_subsections(section)
		folder = DocumentFolder(
			"api",
			f"{self.app_name}/docs",
			[
				section,
			],
		)

		project_manager = ProjectManager(
			f"{self.app_name}",
			"Project Web Application",
			"Project application based on pyEchoNext web-framework",
			f"{self.app_name}",
			f"{self.app_name}",
			f"{self.app_name}",
			ProjectTemplate.BASE,
			[folder],
			[section],
		)

		project_manager.process_project()

	def _generate_introduction(self) -> InitiationSection:
		"""
		Generate introduction

		:returns:	The initiation section.
		:rtype:		InitiationSection
		"""
		section = InitiationSection(
			f"Project {self.app_name}",
			f"Project Documentation for {self.app_name}",
			{"Routes": ", ".join(self.app.routes.keys())},
		)
		return section

	def _generate_subsections(self, section: DocumentSection):
		"""
		Generate subsections

		:param		section:  The section
		:type		section:  DocumentSection
		"""
		subsections = []

		for path, data in self.pages.items():
			subsections.append(
				RoutesSubsection(
					path,
					{
						"Route": f'Methods: {data["methods"]}\n\nReturn type: {data["return_type"]}',
						"Extra": f'Extra: {"\n".join([f" + {key}: {value}" for key, value in data["extra"].items()])}',
					},
					section,
				)
			)

		for subsection in subsections:
			section.link_new_subsection(subsection)

	def documentate_route(
		self,
		page_path: str,
		return_type: Any,
		params: dict,
		methods: list,
		extra: dict = {},
	) -> Callable:
		"""
		Add routed page to documentation

		:param		page_path:	  The page path
		:type		page_path:	  str
		:param		return_type:  The return type
		:type		return_type:  Any
		:param		params:		  The parameters
		:type		params:		  dict
		:param		methods:	  The methods
		:type		methods:	  list
		:param		extra:		  The extra
		:type		extra:		  dict

		:returns:	wrapper handler
		:rtype:		Callable
		"""
		if page_path in self.pages:
			return

		def wrapper(handler):
			"""
			Wrapper for handler

			:param		handler:  The handler
			:type		handler:  callable

			:returns:	handler
			:rtype:		callable
			"""
			self.pages[page_path] = {
				"page_path": page_path,
				"doc": handler.__doc__,
				"funcname": handler.__name__,
				"return_type": return_type,
				"params": params,
				"methods": methods,
				"extra": extra,
			}
			return handler

		return wrapper
```

Для добавления роута в документацию просто к нужному хендлеру добавьте декоратор documentate_route, примерно так: 

```python
@projdoc.documentate_route('/book', str, {}, ['GET', 'POST'])
```

Собственно, секции документации это и есть роуты.

## Генерация документации API
Генерация API будет происходить в двух этапах: генерация спефикации OpenAPI и генерация к нему html-шаблона.

OpenAPI спецификация (OAS, OpenAPI Specification) определяет формализованный стандарт, который описывает интерфейс к REST API сревису и позволяет определять возможности REST-сервиса без доступа к его исходному коду или документации.

[Спецификация 3.0.0 более подробнее.](https://spec.openapis.org/oas/v3.0.0.html)

В нашем коде выглядит она будет выглядеть примерно так:

```python
spec = {
		"openapi": "3.0.0",
		"info": {
			"title": self._app.app_name,
			"version": self._app.settings.VERSION,
			"description": self._app.settings.DESCRIPTION,
		},
		"paths": {

		},
	}
```

В paths мы будем добавлять пути, которые будут браться из обработчиков маршрутов.

<details>
	<summary>Код для генерации спецификации</summary>

```python
class APIDocumentation:
	"""
	This class describes an API documentation.
	"""

	def __init__(self, app: "EchoNext"):
		"""
		Constructs a new instance.

		:param		app:  The application
		:type		app:  EchoNext
		"""
		self._app = app

	def init_app(self, app: "EchoNext"):
		"""
		Initializes the application.

		:param		app:  The application
		:type		app:  EchoNext
		"""
		self._app = app

	def generate_spec(self) -> str:
		"""
		Generate OpenAPI specficiation from app routes&views

		:returns:	jsonfied openAPI API specification
		:rtype:		str
		"""
		spec = {
			"openapi": "3.0.0",
			"info": {
				"title": self._app.app_name,
				"version": self._app.settings.VERSION,
				"description": self._app.settings.DESCRIPTION,
			},
			"paths": {},
		}

		for url in self._app.urls:
			spec["paths"][url.url] = {
				"get": {
					"summary": str(f'{url.view.__doc__}. {url.view.get.__doc__}').replace('\n', '<br>')
					.strip(),
					"responses": {"200": {"description": "Successful response"}, "405": {"description": "Method not allow"}},
				},
				"post": {
					"summary": str(f'{url.view.__doc__}. {url.view.post.__doc__}').replace('\n', '<br>')
					.strip(),
					"responses": {"200": {"description": "Successful response"}, "405": {"description": "Method not allow"}},
				}
			}

		for path, handler in self._app.routes.items():
			spec["paths"][path] = {
				"get": {
					"summary": str(handler.__doc__)
					.strip()
					.replace("\n", ".")
					.replace("\t", ";"),
					"responses": {"200": {"description": "Successful response"}, "405": {"description": "Method not allow"}},
				},
				"post": {
					"summary": str(handler.__doc__)
					.strip()
					.replace("\n", ".")
					.replace("\t", ";"),
					"responses": {"200": {"description": "Successful response"}, "405": {"description": "Method not allow"}},
				}
			}

		return spec
```
</details>

А для того чтобы мы могли просматривать как веб-страницу, создадим генератор html-шаблона

<details>
	<summary>Генератор HTML-шаблона</summary>

```python



class APIDocUI:
	"""
	This class describes an api document ui.
	"""

	def __init__(self, specification: dict):
		"""
		Constructs a new instance.

		:param      specification:  The specification
		:type       specification:  dict
		"""
		self.specification = specification

	def generate_section(self, route: str, summary_get: str, 
		summary_post: str, get_responses: dict, post_responses: dict) -> str:
		"""
		generate section

		:param      route:           The route
		:type       route:           str
		:param      summary_get:     The summary get
		:type       summary_get:     str
		:param      summary_post:    The summary post
		:type       summary_post:    str
		:param      get_responses:   The get responses
		:type       get_responses:   dict
		:param      post_responses:  The post responses
		:type       post_responses:  dict

		:returns:   template section
		:rtype:     str
		"""

		template = f'''
<div class="section">
		<div class="section-header">
			<span>{route}</span>
			<span class="collapse-icon">➡️</span>
		</div>
		<div class="section-content">
			<div class="method">
				<strong>GET</strong>
				<p>{summary_get}</p>
				<div class="responses">
					{"".join([f"<div class='response-item'>{key}: {value["description"]}.</div>" for key, value in get_responses.items()])}
				</div>
			</div>
			<div class="method">
				<strong>POST</strong>
				<p>{summary_post}</p>
				<div class="responses">
					<div class="responses">
					{"".join([f"<div class='response-item'>{key}: {value["description"]}.</div>" for key, value in post_responses.items()])}
				</div>
				</div>
			</div>
		</div>
	</div>
		           '''

		return template

	def generate_html_page(self) -> str:
		"""
		Generate html page template

		:returns:   template
		:rtype:     str
		"""
		template = '''
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>API Documentation</title>
	<style>
		body {
			font-family: Arial, sans-serif;
			margin: 0;
			padding: 0;
			background-color: #f9f9f9;
			color: #333;
		}
		h1, h2, h3 {
			margin: 0;
			padding: 10px 0;
		}
		.container {
			max-width: 800px;
			margin: 40px auto;
			padding: 20px;
			background: #fff;
			border-radius: 8px;
			box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
		}
		.version {
			font-size: 14px;
			color: #555;
			margin-bottom: 20px;
		}
		.info-section {
			border-bottom: 1px solid #ddd;
			padding-bottom: 20px;
			margin-bottom: 20px;
		}
		.section {
			border-radius: 5px;
			overflow: hidden;
			margin-bottom: 20px;
			transition: box-shadow 0.3s ease;
		}
		.section-header {
			padding: 15px;
			background: #007bff;
			color: white;
			cursor: pointer;
			position: relative;
			font-weight: bold;
			display: flex;
			justify-content: space-between;
			align-items: center;
		}
		.section-content {
			padding: 15px;
			display: none;
			overflow: hidden;
			background-color: #f1f1f1;
		}
		.method {
			border-bottom: 1px solid #ddd;
			padding: 10px 0;
		}
		.method:last-child {
			border-bottom: none;
		}
		.responses {
			margin-top: 10px;
			padding-left: 15px;
			font-size: 14px;
			color: #555;
		}
		.response-item {
			margin-bottom: 5px;
		}
		.collapse-icon {
			transition: transform 0.3s;
		}
		.collapse-icon.collapsed {
			transform: rotate(90deg);
		}
		.section:hover {
			box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
		}
	</style>
</head>
<body>

<div class="container">
	<h1>OpenAPI Documentation</h1>
	<h2>PyEchoNext Web Application</h2>
	<div class="version">OpenAPI Version: {{openapi-version}}</div>
	<div class="info-section">
		<h2>Application Information</h2>
		<p><strong>Title:</strong> {{info_title}}</p>
		<p><strong>Version:</strong> {{info_version}}</p>
		<p><strong>Description:</strong> {{info_description}}</p>
	</div>

	{{sections}}

<script>
	document.querySelectorAll('.section-header').forEach(header => {
		header.addEventListener('click', () => {
			const content = header.nextElementSibling;
			const icon = header.querySelector('.collapse-icon');

			if (content.style.display === "block") {
				content.style.display = "none";
				icon.classList.add('collapsed');
			} else {
				content.style.display = "block";
				icon.classList.remove('collapsed');
			}
		});
	});
</script>

</body>
</html>
				   '''

		content = {
			'{{openapi-version}}': self.specification['openapi'],
			"{{info_title}}": self.specification["info"]["title"],
			"{{info_version}}": self.specification["info"]["version"],
			"{{info_description}}": self.specification["info"]["description"],
			"{{sections}}": "\n".join([self.generate_section(path,
											value['get']['summary'], value['post']['summary'], 
											value['get']['responses'], 
											value['post']['responses']) for path, value in self.specification["paths"].items()])
		}

		for key, value in content.items():
			template = template.replace(key, value)

		return template
```

</details>

# Конфигурация и загрузка настроек
Нашему приложению нужна будет конфигурация, такие как мета-информация или настройка директорий для работы и других вещей.

Также я решил сделать конфигурацию универсальной - ее можно будет загружать из .ini, переменных окружения или python-файла.

Сам класс настроек будет передоваться в конструктор нашего будущего класса приложения. Выглядит он так:

```python
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
```

 + BASE_DIR - базовая диреткория проекта
 + TEMPLATES_DIR - директория html-шаблонов
 + SECRET_KEY - секретный ключ
 + VERSION - версия
 + DESCRIPTION - описание
 + LOCALE - код локализации
 + LOCALE_DIR - директория с файлами локализаций.

Для загрузки .ini мы будем использовать configparser, для переменных окружения python-dotenv, а для python-файлов importlib.

<details>
	<summary>Исходный код config.py</summary>	

```python
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
```
</details>

Примеры загрузки конфига:

### DOTENV

```python
config_loader = SettingsLoader(SettingsConfigType.DOTENV, 'example_env')
settings = config_loader.get_settings()
```

Файл example_env:

```env
PEN_BASE_DIR=.
PEN_TEMPLATES_DIR=templates
PEN_SECRET_KEY=secret-key
PEN_LOCALE=RU_RU
PEN_LOCALE_DIR=locales
PEN_VERSION=1.0.0
PEN_DESCRIPTION=Example
```

### INI

```python
config_loader = SettingsLoader(SettingsConfigType.INI, 'example_ini.ini')
settings = config_loader.get_settings()
```

Файл example_ini.ini:

```ini
[Settings]
BASE_DIR=.
TEMPLATES_DIR=templates
SECRET_KEY=secret-key
LOCALE=DEFAULT
VERSION=1.0.0
DESCRIPTION=Example
```

### PyModule

```python
config_loader = SettingsLoader(SettingsConfigType.PYMODULE, 'example_module.py')
settings = config_loader.get_settings()
```

Файл example_module.py:

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = 'templates'
SECRET_KEY = 'secret-key'
VERSION = '1.0.0'
DESCRIPTION = 'Echonext webapp'
LOCALE = 'DEFAULT'
LOCALE_DIR = None
```

# Рендер html-шаблонов
Я решил небольшой встроенный движок и интегрировать Jinja2.

Начнем с встроенного. Он будет основан на regex-выражениях. На данный момент я реализовал два:

```python
FOR_BLOCK_PATTERN = re.compile(
	r"{% for (?P<variable>[a-zA-Z]+) in (?P<seq>[a-zA-Z]+) %}(?P<content>[\S\s]+)(?={% endfor %}){% endfor %}"
)
VARIABLE_PATTERN = re.compile(r"{{ (?P<variable>[a-zA-Z_]+) }}")
```

Он похож на Jinja2. Для for-цикла нужно использовать конструкцию `{% for ... in ... %}{% endfor %}`, а для вывода переменных `{{ <переменная> }}`.

Директория с шаблонами будет браться из класса настроек.

Для генерации будет создана функция `render_template(request: Request, template_name: str, **kwargs)`. Ей нужен Request, имя шаблона (без директории), а также контекст - то есть kwargs. То есть при вызове `render_template(request, 'index.html', name="Vasya")` в шаблоне можно использовать будет переменную name.

<details>
	<summary>Встроенный шаблонизатор</summary>

```python
import os
import re
from loguru import logger
from pyechonext.request import Request
from pyechonext.utils.exceptions import TemplateNotFileError

FOR_BLOCK_PATTERN = re.compile(
	r"{% for (?P<variable>[a-zA-Z]+) in (?P<seq>[a-zA-Z]+) %}(?P<content>[\S\s]+)(?={% endfor %}){% endfor %}"
)
VARIABLE_PATTERN = re.compile(r"{{ (?P<variable>[a-zA-Z_]+) }}")


class TemplateEngine:
	"""
	This class describes a built-in template engine.
	"""

	def __init__(self, base_dir: str, templates_dir: str):
		"""
		Constructs a new instance.

		:param		base_dir:		The base dir
		:type		base_dir:		str
		:param		templates_dir:	The templates dir
		:type		templates_dir:	str
		"""
		self.templates_dir = os.path.join(base_dir, templates_dir)

	def _get_template_as_string(self, template_name: str) -> str:
		"""
		Gets the template as string.

		:param		template_name:		   The template name
		:type		template_name:		   str

		:returns:	The template as string.
		:rtype:		str

		:raises		TemplateNotFileError:  Template is not a file
		"""
		template_name = os.path.join(self.templates_dir, template_name)

		if not os.path.isfile(template_name):
			raise TemplateNotFileError(f'Template "{template_name}" is not a file')

		with open(template_name, "r") as file:
			content = file.read()

		return content

	def _build_block_of_template(self, context: dict, raw_template_block: str) -> str:
		"""
		Builds a block of template.

		:param		context:			 The context
		:type		context:			 dict
		:param		raw_template_block:	 The raw template block
		:type		raw_template_block:	 str

		:returns:	The block of template.
		:rtype:		str
		"""
		used_vars = VARIABLE_PATTERN.findall(raw_template_block)

		if used_vars is None:
			return raw_template_block

		for var in used_vars:
			var_in_template = "{{ %s }}" % (var)
			processed_template_block = re.sub(
				var_in_template, str(context.get(var, "")), raw_template_block
			)

		return processed_template_block

	def _build_statement_for_block(self, context: dict, raw_template_block: str) -> str:
		"""
		Build statement `for` block

		:param		context:			 The context
		:type		context:			 dict
		:param		raw_template_block:	 The raw template block
		:type		raw_template_block:	 str

		:returns:	The statement for block.
		:rtype:		str
		"""
		statement_for_block = FOR_BLOCK_PATTERN.search(raw_template_block)

		if statement_for_block is None:
			return raw_template_block

		builded_statement_block_for = ""

		for variable in context.get(statement_for_block.group("seq"), []):
			builded_statement_block_for += self._build_block_of_template(
				{**context, statement_for_block.group("variable"): variable},
				statement_for_block.group("content"),
			)

		processed_template_block = FOR_BLOCK_PATTERN.sub(
			builded_statement_block_for, raw_template_block
		)

		return processed_template_block

	def build(self, context: dict, template_name: str) -> str:
		"""
		Build template

		:param		context:		The context
		:type		context:		dict
		:param		template_name:	The template name
		:type		template_name:	str

		:returns:	raw template string
		:rtype:		str
		"""
		raw_template = self._get_template_as_string(template_name)

		processed_template = self._build_statement_for_block(context, raw_template)

		return self._build_block_of_template(context, processed_template)


def render_template(request: Request, template_name: str, **kwargs) -> str:
	"""
	Render template

	:param		request:		 The request
	:type		request:		 Request
	:param		template_name:	 The template name
	:type		template_name:	 str
	:param		kwargs:			 The keywords arguments
	:type		kwargs:			 dictionary

	:returns:	raw template string
	:rtype:		str

	:raises		AssertionError:	 BASE_DIR and TEMPLATES_DIR is empty
	"""
	logger.warn(
		"Built-in template engine is under development and may be unstable or contain bugs"
	)

	assert request.settings.BASE_DIR
	assert request.settings.TEMPLATES_DIR

	engine = TemplateEngine(request.settings.BASE_DIR, request.settings.TEMPLATES_DIR)

	context = kwargs

	logger.debug(f"Built-in template engine: render {template_name} ({request.path})")

	return engine.build(context, template_name)
```
</details>

Для Jinja2 будет очень похожий код, для того чтобы не было проблем с поддержкой.

<details>
	<summary>Код интеграции Jinja2</summary>

```python
from os.path import join, exists, getmtime
from jinja2 import BaseLoader, TemplateNotFound
from jinja2 import Environment, select_autoescape
from loguru import logger
from pyechonext.request import Request


class TemplateLoader(BaseLoader):
	"""
	This class describes a jinja2 template loader.
	"""

	def __init__(self, path: str):
		"""
		Constructs a new instance.

		:param		path:  The path
		:type		path:  str
		"""
		self.path = path

	def get_source(self, environment, template):
		path = join(self.path, template)

		if not exists(path):
			raise TemplateNotFound(template)

		mtime = getmtime(path)

		with open(path) as f:
			source = f.read()

		return source, path, lambda: mtime == getmtime(path)


class TemplateEngine:
	"""
	This class describes a jinja template engine.
	"""

	def __init__(self, base_dir: str, templates_dir: str):
		"""
		Constructs a new instance.

		:param		base_dir:		The base dir
		:type		base_dir:		str
		:param		templates_dir:	The templates dir
		:type		templates_dir:	str
		"""
		self.base_dir = base_dir
		self.templates_dir = join(base_dir, templates_dir)
		self.env = Environment(
			loader=TemplateLoader(self.templates_dir), autoescape=select_autoescape()
		)

	def build(self, template_name: str, **kwargs):
		template = self.env.get_template(template_name)

		return template.render(**kwargs)


def render_template(request: Request, template_name: str, **kwargs) -> str:
	"""
	Render template

	:param		request:		 The request
	:type		request:		 Request
	:param		template_name:	 The template name
	:type		template_name:	 str
	:param		kwargs:			 The keywords arguments
	:type		kwargs:			 dictionary

	:returns:	raw template string
	:rtype:		str

	:raises		AssertionError:	 BASE_DIR and TEMPLATES_DIR is empty
	"""
	assert request.settings.BASE_DIR
	assert request.settings.TEMPLATES_DIR

	engine = TemplateEngine(request.settings.BASE_DIR, request.settings.TEMPLATES_DIR)

	logger.debug(f"Jinja2 template engine: render {template_name} ({request.path})")

	return engine.build(template_name, **kwargs)
```
</details>

# Ответ-запрос

 > Будь ты в Рыбацкино, или южный Бромс. Если есть реквест, значит есть респонс.

В информатике запрос-ответ или запрос-реплика - это один из основных методов, используемых компьютерами для связи друг с другом в сети, при котором первый компьютер отправляет запрос на некоторые данные, а второй отвечает на запрос. Более конкретно, это шаблон обмена сообщениями, при котором запрашивающий отправляет сообщение с запросом системе-ответчику, которая получает и обрабатывает запрос, в конечном счете возвращая сообщение в ответ. Это аналогично телефонному звонку, при котором вызывающий абонент должен дождаться, пока получатель возьмет трубку, прежде чем что-либо можно будет обсудить.

## Request
**Request** — это запрос, который содержит данные для взаимодействия между клиентом и API: базовый URL, конечную точку, используемый метод, заголовки и т. д.

Сам класс выглядит так:

```python
class Request:
	"""
	This class describes a request.
	"""

	def __init__(self, environ: dict, settings: Settings):
		"""
		Constructs a new instance.

		:param		environ:  The environ
		:type		environ:  dict
		"""
		self.environ: dict = environ
		self.settings: Settings = settings
		self.method: str = self.environ["REQUEST_METHOD"]
		self.path: str = self.environ["PATH_INFO"]
		self.GET: dict = self._build_get_params_dict(self.environ["QUERY_STRING"])
		self.POST: dict = self._build_post_params_dict(self.environ["wsgi.input"].read())
		self.user_agent: str = self.environ["HTTP_USER_AGENT"]
		self.extra: dict = {}

		logger.debug(f"New request created: {self.method} {self.path}")

	def __getattr__(self, item: Any) -> Union[Any, None]:
		"""
		Magic method for get attrs (from extra)

		:param		item:  The item
		:type		item:  Any

		:returns:	Item from self.extra or None
		:rtype:		Union[Any, None]
		"""
		return self.extra.get(item, None)

	def _build_get_params_dict(self, raw_params: str):
		"""
		Builds a get parameters dictionary.

		:param		raw_params:	 The raw parameters
		:type		raw_params:	 str
		"""
		return parse_qs(raw_params)

	def _build_post_params_dict(self, raw_params: bytes):
		"""
		Builds a post parameters dictionary.

		:param		raw_params:	 The raw parameters
		:type		raw_params:	 bytes
		"""
		return parse_qs(raw_params.decode())
```

Request требует следующие аргументы для создания:

 + environ (словарь) - веб-окружение (генерируется gunicorn)
 + settings (объект датакласса pyechonext.config.Settings)

Request имеет следующие публичные атрибуты:

 + environ (словарь) - веб-окружение
 + settings (объект датакласса pyechonext.config.Settings)
 + method (строка) - http-метод
 + path (строка) - путь
 + GET (словарь) - параметры get-запроса
 + POST (словарь) - параметры post-запроса
 + user_agent (строка) - User-Agent
 + extra (словарь) - дополнительные параметры (например для middleware)

Request также имеет следующие методы:
 
 + `__getattr__` - магический метод дескриптора для получения атрибутов (для получения элементов из атрибута extra)
 + `_build_get_params_dict` - приватный метод для парсинга параметров get-запроса
 + `_build_post_params_dict` - приватный метод для парсинга параметров post-запроса

## Response
**Response** — это ответ, который содержит данные, возвращаемые сервером, в том числе контент, код состояния и заголовки.

```python
import json
from typing import Dict, Iterable, Union, Any, List, Tuple, Optional
from socks import method
from loguru import logger
from pyechonext.request import Request


class Response:
	"""
	This dataclass describes a response.
	"""

	default_content_type: str = "text/html"
	default_charset: str = "UTF-8"
	unicode_errors: str = "strict"
	default_conditional_response: bool = False
	default_body_encoding: str = "UTF-8"

	def __init__(
		self,
		request: Request,
		use_i18n: bool = False,
		status_code: Optional[int] = 200,
		body: Optional[str] = None,
		headers: Optional[Dict[str, str]] = {},
		content_type: Optional[str] = None,
		charset: Optional[str] = None,
		**kwargs,
	):
		"""
		Constructs a new instance.

		:param		request:	   The request
		:type		request:	   Request
		:param		use_i18n:	   The use i 18 n
		:type		use_i18n:	   bool
		:param		status_code:   The status code
		:type		status_code:   int
		:param		body:		   The body
		:type		body:		   str
		:param		headers:	   The headers
		:type		headers:	   Dict[str, str]
		:param		content_type:  The content type
		:type		content_type:  str
		:param		charset:	   The charset
		:type		charset:	   str
		:param		kwargs:		   The keywords arguments
		:type		kwargs:		   dictionary
		"""
		if status_code == 200:
			self.status_code: str = "200 OK"
		else:
			self.status_code: str = str(status_code)

		if content_type is None:
			self.content_type: str = self.default_content_type
		else:
			self.content_type: str = content_type

		if charset is None:
			self.charset: str = self.default_charset
		else:
			self.charset: str = charset

		if body is not None:
			self.body: str = body
		else:
			self.body: str = ""

		self._headerslist: list = headers
		self._added_headers: list = []
		self.request: Request = request
		self.extra: dict = {}

		self.use_i18n: bool = use_i18n
		self.i18n_kwargs = kwargs

		self._update_headers()

	def __getattr__(self, item: Any) -> Union[Any, None]:
		"""
		Magic method for get attrs (from extra)

		:param		item:  The item
		:type		item:  Any

		:returns:	Item from self.extra or None
		:rtype:		Union[Any, None]
		"""
		return self.extra.get(item, None)

	def _structuring_headers(self, environ):
		headers = {
			"Host": environ["HTTP_HOST"],
			"Accept": environ["HTTP_ACCEPT"],
			"User-Agent": environ["HTTP_USER_AGENT"],
		}

		for name, value in headers.items():
			self._headerslist.append((name, value))

		for header_tuple in self._added_headers:
			self._headerslist.append(header_tuple)

	def _update_headers(self) -> None:
		"""
		Sets the headers by environ.

		:param		environ:  The environ
		:type		environ:  dict
		"""
		self._headerslist = [
			("Content-Type", f"{self.content_type}; charset={self.charset}"),
			("Content-Length", str(len(self.body))),
		]

	def add_headers(self, headers: List[Tuple[str, str]]):
		"""
		Adds new headers.

		:param		headers:  The headers
		:type		headers:  List[Tuple[str, str]]
		"""
		for header in headers:
			self._added_headers.append(header)

	def _encode_body(self):
		"""
		Encodes a body.
		"""
		if self.content_type.split("/")[-1] == "json":
			self.body = str(self.json)

		try:
			self.body = self.body.encode("UTF-8")
		except AttributeError:
			self.body = str(self.body).encode("UTF-8")

	def __call__(self, environ: dict, start_response: method) -> Iterable:
		"""
		Makes the Response object callable.

		:param		environ:		 The environ
		:type		environ:		 dict
		:param		start_response:	 The start response
		:type		start_response:	 method

		:returns:	response body
		:rtype:		Iterable
		"""
		self._encode_body()

		self._update_headers()
		self._structuring_headers(environ)

		logger.debug(
			f"[{environ['REQUEST_METHOD']} {self.status_code}] Run response: {self.content_type}"
		)

		start_response(status=self.status_code, headers=self._headerslist)

		return iter([self.body])

	@property
	def json(self) -> dict:
		"""
		Parse request body as JSON.

		:returns:	json body
		:rtype:		dict
		"""
		if self.body:
			if self.content_type.split("/")[-1] == "json":
				return json.dumps(self.body)
			else:
				return json.dumps(self.body.decode("UTF-8"))

		return {}

	def __repr__(self):
		"""
		Returns a unambiguous string representation of the object (for debug...).

		:returns:	String representation of the object.
		:rtype:		str
		"""
		return f"<{self.__class__.__name__} at 0x{abs(id(self)):x} {self.status_code}>"
```

Response имеет следующие аргументы:

 + request (объект класса Request) - запрос
 + [опционально] status_code (целочисленное значение) - статус-код ответа
 + [опционально] body (строка) - тело ответа
 + [опционально] headers (словарь) - заголовки ответа
 + [опционально] content_type (строка) - тип контента ответа
 + [опционально] charset (строка) - кодировка ответа
 + [опционально] use_i18n (логическое значение) - использовать ли i18n (по умолчанию False)

Response имеет следующие атрибуты:

 + status_code (строка) - статус-код (по умолчанию "200 OK")
 + content_type (строка) - контент-тип (по умолчанию равен значению default_content_type)
 + charset (строка) - кодировка (по умолчанию равен значению default_charset)
 + body (строка) - тело овтета (по умолчанию равен пустой строке)
 + `_headerslist` (список) - приватный список заголовков ответа
 + `_added_headers` (список) - приватный список добавленных заголовков ответа
 + request (объект класса Request) - запрос
 + extra (словарь) - дополнительные параметры

Response имеет следующие методы:

 + `__getattr__` - магический метод дескриптора для получения атрибутов (для получения элементов из атрибута extra)
 + `_structuring_headers` - приватный метод структуирования заголовков из веб-окружения
 + `_update_headers` - приватный метод обновления (перезаписывания) списков заголовков
 + `add_headers` - публичный метод добавления заголовков
 + `_encode_body` - кодирование тела ответа
 + `__call__` - магический метод, делает объект Response вызываемым
 + `json` - свойство класса для получения тела ответа в виде json

# Views (обработчики)

View - это и есть абстракция маршрута сайта (django-like). Он обязательно должен иметь два метода: `get` и `post` (для ответа на get и post запросы). Эти методы должны возвращать:

 + Данные, контент страницы. Это может быть словарь или строка.

ИЛИ:

 + Объект класса Response (pyechonext.response)

View представляет собой объект класса View:

```python
class View(ABC):
	"""
	Page view
	"""

	@abstractmethod
	def get(
		self, request: Request, response: Response, *args, **kwargs
	) -> Union[Response, Any]:
		"""
		Get

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		args:	   The arguments
		:type		args:	   list
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary
		"""
		raise NotImplementedError

	@abstractmethod
	def post(
		self, request: Request, response: Response, *args, **kwargs
	) -> Union[Response, Any]:
		"""
		Post

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		args:	   The arguments
		:type		args:	   list
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary
		"""
		raise NotImplementedError
```

И давайте я покажу пример View:

```python
class IndexView(View):
	def get(
		self, request: Request, response: Response, **kwargs
	) -> Union[Response, Any]:
		"""
		Get

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		args:	   The arguments
		:type		args:	   list
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary
		"""
		return "Welcome to pyEchoNext webapplication!"

	def post(
		self, request: Request, response: Response, **kwargs
	) -> Union[Response, Any]:
		"""
		Post

		:param		request:   The request
		:type		request:   Request
		:param		response:  The response
		:type		response:  Response
		:param		args:	   The arguments
		:type		args:	   list
		:param		kwargs:	   The keywords arguments
		:type		kwargs:	   dictionary
		"""
		return "Message has accepted!"
```

# URLS
Для того чтобы подключать Views к приложению, мы создадим слой абстракции - датакласс URL, который будет содержать в себе путь и сам класс View. Причем View нужно передавать без создания объекта, то есть сам класс.

```python
from dataclasses import dataclass
from typing import Type
from pyechonext.views import View, IndexView


@dataclass
class URL:
	"""
	This dataclass describes an url.
	"""

	url: str
	view: Type[View]


url_patterns = [URL(url="/", view=IndexView)]
```

url_patterns - встроенные паттерны. Для примера используем ранее созданный IndexView.

# Middleware (промежуточное ПО)
Итак, для реализации, например, cookie нам нужно будет работать с реквест-респонсом во вребя работы сервера. Для этого мы будем использовать абстракцию промежуточного ПО.

```python
class BaseMiddleware(ABC):
	"""
	This abstract class describes a base middleware.
	"""

	@abstractmethod
	def to_request(self, request: Request):
		"""
		To request method

		:param		request:  The request
		:type		request:  Request
		"""
		raise NotImplementedError

	@abstractmethod
	def to_response(self, response: Response):
		"""
		To response method

		:param		response:  The response
		:type		response:  Response
		"""
		raise NotImplementedError
```

Он имеет два абстрактных метода - to_request и to_response.

Давайте реализуем базовый Middleware сессии для добавления cookie:

```python
class SessionMiddleware(BaseMiddleware):
	"""
	This class describes a session (cookie) middleware.
	"""

	def to_request(self, request: Request):
		"""
		Set to request

		:param		request:  The request
		:type		request:  Request
		"""
		cookie = request.environ.get("HTTP_COOKIE", None)

		if not cookie:
			return

		session_id = parse_qs(cookie)["session_id"][0]
		logger.debug(
			f"Set session_id={session_id} for request {request.method} {request.path}"
		)
		request.extra["session_id"] = session_id

	def to_response(self, response: Response):
		"""
		Set to response

		:param		response:  The response
		:type		response:  Response
		"""
		if not response.request.session_id:
			session_id = uuid4()
			logger.debug(
				f"Set session_id={session_id} for response {response.status_code} {response.request.path}"
			)
			response.add_headers(
				[
					("Set-Cookie", f"session_id={session_id}"),
				]
			)


middlewares = [SessionMiddleware] # Список мидлварей
```

И теперь займемся самим app.py - приложением.

# Утилиты
Нам нужно создать файл `utils/__init__.py`, в котором будет находиться небольшая вспомогательная функция `_prepare_url`. Она будет обрезать URL от всего лишнего:

```python
from datetime import datetime


def get_current_datetime() -> str:
	"""
	Gets the current datetime.

	:returns:	The current datetime.
	:rtype:		str
	"""
	date = datetime.now()
	return date.strftime("%Y-%m-%d %H:%M:%S")


def _prepare_url(url: str) -> str:
	"""
	Prepare URL (remove ending /)

	:param		url:  The url
	:type		url:  str

	:returns:	prepared url
	:rtype:		str
	"""
	try:
		if url[-1] == "/" and len(url) > 1:
			return url[:-1]
	except IndexError:
		return "/"

	return url
```

# Приложение
Основой является класс EchoNext (pyechonext.app).

Давайте создадим его.

Импортируем все нужные модули:

```python
import inspect
from enum import Enum
from typing import Iterable, Callable, List, Type, Tuple, Optional, Union
from dataclasses import dataclass
from socks import method
from parse import parse
from loguru import logger
from pyechonext.urls import URL
from pyechonext.views import View
from pyechonext.request import Request
from pyechonext.response import Response
from pyechonext.utils.exceptions import (
	RoutePathExistsError,
	MethodNotAllow,
	URLNotFound,
	WebError,
	TeapotError,
)
from pyechonext.utils import _prepare_url
from pyechonext.config import Settings
from pyechonext.middleware import BaseMiddleware
from pyechonext.i18n_l10n.i18n import JSONi18nLoader
from pyechonext.i18n_l10n.l10n import JSONLocalizationLoader
```

Создадим датакласс типа приложения:

```python
class ApplicationType(Enum):
	"""
	This enum class describes an application type.
	"""

	JSON = "application/json"
	HTML = "text/html"
	PLAINTEXT = "text/plain"
	TEAPOT = "server/teapot"
```

 + JSON - в основном для API
 + HTML - для полноценного веб-сайта
 + PLAINTEXT - просто текст

После создадим датакласс HistoryEntry для хранения истории запросов-ответов:

```python
@dataclass
class HistoryEntry:
	request: Request
	response: Response
```

Давайте начнем создавать класс приложения:

```python
class EchoNext:
	"""
	This class describes an EchoNext WSGI Application.
	"""

	__slots__ = (
		"app_name",
		"settings",
		"middlewares",
		"application_type",
		"urls",
		"routes",
		"i18n_loader",
		"l10n_loader",
		"history",
	)
```

`__slots__` - это слоты (атрибуты класса перечислены в кортеже). Это механизм, который позволяет оптимизировать использование памяти и ускорить доступ к атрибутам класса. Когда вы создаете объект класса в Python, интерпретатор выделяет память для хранения всех атрибутов этого объекта.

После этого создадим магический метод конструктора класса:

```python
def __init__(
		self,
		app_name: str,
		settings: Settings,
		middlewares: List[Type[BaseMiddleware]],
		urls: Optional[List[URL]] = [],
		application_type: Optional[ApplicationType] = ApplicationType.JSON,
	):
		"""
		Constructs a new instance.

		:param		app_name:		   The application name
		:type		app_name:		   str
		:param		settings:		   The settings
		:type		settings:		   Settings
		:param		middlewares:	   The middlewares
		:type		middlewares:	   List[BaseMiddleware]
		:param		urls:			   The urls
		:type		urls:			   List[URL]
		:param		application_type:  The application type
		:type		application_type:  Optional[ApplicationType]
		"""
		self.app_name = app_name
		self.settings = settings
		self.middlewares = middlewares
		self.application_type = application_type
		self.routes = {}
		self.urls = urls
		self.history: List[HistoryEntry] = []
		self.i18n_loader = JSONi18nLoader(
			self.settings.LOCALE, self.settings.LOCALE_DIR
		)
		self.l10n_loader = JSONLocalizationLoader(
			self.settings.LOCALE, self.settings.LOCALE_DIR
		)
		logger.debug(f"Application {self.application_type.value}: {self.app_name}")

		if self.application_type == ApplicationType.TEAPOT:
			raise TeapotError("Where's my coffie?")
```

Разберем атрибуты:

 + app_name - имя приложения
 + settings - экземпляр датакласса Settings
 + middlewares - список миддлварей
 + application_type - тип приложения
 + routes - словарь с маршрутами, которые были заданы через декоратор route_page (flask-like путь, рассмотрим позже)
 + urls - список URLs (для интеграции View)
 + history - список из HistoryEntry. История запросов-ответов
 + i18n_loader - загрузчик i18n
 + l10n_loader - загрузчик l10n

Реализуем следующий метод:

```python
	def _find_view(self, raw_url: str) -> Union[Type[URL], None]:
		"""
		Finds a view by raw url.

		:param		raw_url:  The raw url
		:type		raw_url:  str

		:returns:	URL dataclass
		:rtype:		Type[URL]
		"""
		url = _prepare_url(raw_url)

		for path in self.urls:
			if url == _prepare_url(path.url):
				return path

		return None
```

Он нужен для нахождения view по сырому URL. Если он найден, возвращаем URL, иначе None.

Создадим метод `_check_request_method`:

```python
	def _check_request_method(self, view: View, request: Request):
		"""
		Check request method for view

		:param		view:			 The view
		:type		view:			 View
		:param		request:		 The request
		:type		request:		 Request

		:raises		MethodNotAllow:	 Method not allow
		"""
		if not hasattr(view, request.method.lower()):
			raise MethodNotAllow(f"Method not allow: {request.method}")
```

Этот метод просто проверяет, доступен ли метод в View.

```python
	def _get_view(self, request: Request) -> View:
		"""
		Gets the view.

		:param		request:  The request
		:type		request:  Request

		:returns:	The view.
		:rtype:		View
		"""
		url = request.path

		return self._find_view(url)
```

Метод выше получает по пути запроса View.

Следующие два метода генерируют запрос и ответ:

```python
	def _get_request(self, environ: dict) -> Request:
		"""
		Gets the request.

		:param		environ:  The environ
		:type		environ:  dict

		:returns:	The request.
		:rtype:		Request
		"""
		return Request(environ, self.settings)

	def _get_response(self, request: Request) -> Response:
		"""
		Gets the response.

		:returns:	The response.
		:rtype:		Response
		"""
		return Response(request, content_type=self.application_type.value)
```

Теперь реализуем тот самый декоратор route_page:

```python
	def route_page(self, page_path: str) -> Callable:
		"""
		Creating a New Page Route

		:param		page_path:	The page path
		:type		page_path:	str

		:returns:	wrapper handler
		:rtype:		Callable
		"""
		if page_path in self.routes:
			raise RoutePathExistsError("Such route already exists.")

		def wrapper(handler):
			"""
			Wrapper for handler

			:param		handler:  The handler
			:type		handler:  callable

			:returns:	handler
			:rtype:		callable
			"""
			self.routes[page_path] = handler
			return handler

		return wrapper
```

Теперь создадим два метода для применения миддлварей к реквесту:

```python
	def _apply_middleware_to_request(self, request: Request):
		"""
		Apply middleware to request

		:param		request:  The request
		:type		request:  Request
		"""
		for middleware in self.middlewares:
			middleware().to_request(request)

	def _apply_middleware_to_response(self, response: Response):
		"""
		Apply middleware to response

		:param		response:  The response
		:type		response:  Response
		"""
		for middleware in self.middlewares:
			middleware().to_response(response)
```

Реализуем метод дефолтного ответа. То есть мы будем назначать, например, респонсу код 404 если страница не найдена:

```python
	def _default_response(self, response: Response, error: WebError) -> None:
		"""
		Get default response (404)

		:param		response:  The response
		:type		response:  Response
		"""
		response.status_code = str(error.code)
		response.body = str(error)
```

Теперь реализуем метод для нахождения хендлера. Кстати, у меня View имеют больший приоритет чем routes:

```python
	def _find_handler(self, request: Request) -> Tuple[Callable, str]:
		"""
		Finds a handler.

		:param		request_path:  The request path
		:type		request_path:  str

		:returns:	handler function and parsed result
		:rtype:		Tuple[Callable, str]
		"""
		url = _prepare_url(request.path)

		for path, handler in self.routes.items():
			parse_result = parse(path, url)
			if parse_result is not None:
				return handler, parse_result.named

		view = self._get_view(request)

		if view is not None:
			parse_result = parse(view.url, url)

			if parse_result is not None:
				return view.view, parse_result.named

		return None, None
```

Создадим метод свитча локализации "на лету":

```python
	def switch_locale(self, locale: str, locale_dir: str):
		"""
		Switch to another locale i18n

		:param		locale:		 The locale
		:type		locale:		 str
		:param		locale_dir:	 The locale dir
		:type		locale_dir:	 str
		"""
		logger.info(f"Switch to another locale: {locale_dir}/{locale}")
		self.i18n_loader.locale = locale
		self.i18n_loader.directory = locale_dir
		self.i18n_loader.translations = self.i18n_loader.load_locale(
			self.i18n_loader.locale, self.i18n_loader.directory
		)
		self.l10n_loader.locale = locale
		self.l10n_loader.directory = directory
		self.i18n_loader.locale_settings = self.l10n_loader.load_locale(
			self.l10n_loader.locale, self.l10n_loader.directory
		)
```

Теперь создадим хендер реквеста, который будет все обрабывать, включая нахождение, генерацию ошибок.

```python
	def _handle_request(self, request: Request) -> Response:
		"""
		Handle response from request

		:param		request:  The request
		:type		request:  Request

		:returns:	Response callable object
		:rtype:		Response
		"""
		logger.debug(f"Handle request: {request.path}")
		response = self._get_response(request)

		handler, kwargs = self._find_handler(request)

		if handler is not None:
			if inspect.isclass(handler):
				handler = getattr(handler(), request.method.lower(), None)
				if handler is None:
					raise MethodNotAllow(f"Method not allowed: {request.method}")

			result = handler(request, response, **kwargs)

			if isinstance(result, Response):
				response = result

				if response.use_i18n:
					response.body = self.i18n_loader.get_string(
						response.body, **response.i18n_kwargs
					)
			else:
				response.body = self.i18n_loader.get_string(result)

				if not response.use_i18n:
					response.body = result
		else:
			raise URLNotFound(f'URL "{request.path}" not found.')

		return response
```

И наконец, метод `__call__`. Он сделает наш класс callable, вызываемым.

```python
	def __call__(self, environ: dict, start_response: method) -> Iterable:
		"""
		Makes the application object callable

		:param		environ:		 The environ
		:type		environ:		 dict
		:param		start_response:	 The start response
		:type		start_response:	 method

		:returns:	response body
		:rtype:		Iterable
		"""
		request = self._get_request(environ)
		self._apply_middleware_to_request(request)
		response = self._get_response(request)

		try:
			response = self._handle_request(request)
			self._apply_middleware_to_response(response)
		except URLNotFound as err:
			logger.error(
				"URLNotFound error has been raised: set default response (404)"
			)
			self._apply_middleware_to_response(response)
			self._default_response(response, error=err)
		except MethodNotAllow as err:
			logger.error(
				"MethodNotAllow error has been raised: set default response (405)"
			)
			self._apply_middleware_to_response(response)
			self._default_response(response, error=err)

		self.history.append(HistoryEntry(request=request, response=response))
		return response(environ, start_response)
```

И да, ошибки обрабатываются и будут уведомлять пользователя сайта в некоторых случаях. Например URLNotFound сгенерирует ошибку 404 и так далее. Это даст возможность также разработчику в коде веб-приложения вызывать веб-ошибки.

И в этом же методе происходит финальная работа.

# Примеры
Давайте я напишу несколько примеров.

## Простой вебапп
Генерация документации, и демонстрация регистрации маршрутов разными путями.

```python
import os
from pyechonext.utils.exceptions import MethodNotAllow
from pyechonext.app import ApplicationType, EchoNext
from pyechonext.views import View
from pyechonext.urls import URL, IndexView
from pyechonext.config import SettingsLoader, SettingsConfigType
from pyechonext.template_engine.jinja import render_template
from pyechonext.middleware import middlewares
from pyechonext.docsgen import ProjDocumentation


class UsersView(View):
	def get(self, request, response, **kwargs):
		return render_template(
			request,
			"index.html",
			user_name="User",
			session_id=request.session_id,
			friends=["Bob", "Anna", "John"],
		)

	def post(self, request, response, **kwargs):
		raise MethodNotAllow(f"Request {request.path}: method not allow")


url_patterns = [URL(url="/", view=IndexView), URL(url="/users", view=UsersView)]
config_loader = SettingsLoader(SettingsConfigType.PYMODULE, 'example_module.py')
settings = config_loader.get_settings()
echonext = EchoNext(
	__name__,
	settings,
	middlewares,
	urls=url_patterns,
	application_type=ApplicationType.HTML,
)
apidoc = ProjDocumentation(echonext)


@echonext.route_page("/book")
@apidoc.documentate_route('/book', str, {}, ['GET', 'POST'])
class BooksResource(View):
	"""
	This class describes a books resource.
	"""

	def get(self, request, response, **kwargs):
		"""
		get queries

		:param      request:   The request
		:type       request:   Request
		:param      response:  The response
		:type       response:  Response
		:param      kwargs:    The keywords arguments
		:type       kwargs:    dictionary

		:returns:   result
		:rtype:     str
		"""
		return f"GET Params: {request.GET}"

	def post(self, request, response, **kwargs):
		"""
		post queries

		:param      request:   The request
		:type       request:   Request
		:param      response:  The response
		:type       response:  Response
		:param      kwargs:    The keywords arguments
		:type       kwargs:    dictionary

		:returns:   result
		:rtype:     str
		"""
		return f"POST Params: {request.POST}"


apidoc.generate_documentation()
```

Для этого вам нужен файл templates/index.html и файл example_module.py.

example_module.py - это файл настроек:

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = 'templates'
SECRET_KEY = 'secret-key'
LOCALE = 'DEFAULT'
LOCALE_DIR = None
VERSION = 0.1.0
DESCRIPTION = 'Example echonext webapp'
```

## Локализация и docs-api ui

```python
import os
from pyechonext.utils.exceptions import MethodNotAllow
from pyechonext.app import ApplicationType, EchoNext
from pyechonext.views import View
from pyechonext.urls import URL, IndexView
from pyechonext.config import SettingsLoader, SettingsConfigType
from pyechonext.response import Response
from pyechonext.template_engine.jinja import render_template
from pyechonext.middleware import middlewares
from pyechonext.docsgen import ProjDocumentation
from pyechonext.apidoc_ui import APIDocumentation, APIDocUI


class UsersView(View):
	def get(self, request, response, **kwargs):
		return render_template(
			request,
			"index.html",
			user_name="User",
			session_id=request.session_id,
			friends=["Bob", "Anna", "John"],
		)

	def post(self, request, response, **kwargs):
		raise MethodNotAllow(f"Request {request.path}: method not allow")


url_patterns = [URL(url="/", view=IndexView), URL(url="/users", view=UsersView)]
config_loader = SettingsLoader(SettingsConfigType.PYMODULE, 'el_config.py')
settings = config_loader.get_settings()
echonext = EchoNext(
	__name__,
	settings,
	middlewares,
	urls=url_patterns,
	application_type=ApplicationType.HTML,
)
apidoc = APIDocumentation(echonext)
projdoc = ProjDocumentation(echonext)


@echonext.route_page('/api-docs')
def api_docs(request, response):
	ui = APIDocUI(apidoc.generate_spec())
	return ui.generate_html_page()


@echonext.route_page("/book")
@projdoc.documentate_route('/book', str, {}, ['GET', 'POST'])
class BooksResource(View):
	"""
	This class describes a books resource.
	"""

	def get(self, request, response, **kwargs):
		"""
		get queries

		:param      request:   The request
		:type       request:   Request
		:param      response:  The response
		:type       response:  Response
		:param      kwargs:    The keywords arguments
		:type       kwargs:    dictionary

		:returns:   result
		:rtype:     str
		"""
		return echonext.l10n_loader.format_currency(1305.50)

	def post(self, request, response, **kwargs):
		"""
		post queries

		:param      request:   The request
		:type       request:   Request
		:param      response:  The response
		:type       response:  Response
		:param      kwargs:    The keywords arguments
		:type       kwargs:    dictionary

		:returns:   result
		:rtype:     str
		"""
		return echonext.i18n_loader.get_string('title %{name}', name='Localization Site')


projdoc.generate_documentation()
```

## Пример приложения с БД
Я буду использовать свою собственную ORM - [ссылка на репозиторий](https://github.com/alexeev-prog/SQLSymphony). Устанавливается он просто: `pip3 install sqlsymphony_orm`.

```python
import os
from pyechonext.app import ApplicationType, EchoNext
from pyechonext.config import Settings
from sqlsymphony_orm.datatypes.fields import IntegerField, RealField, TextField
from sqlsymphony_orm.models.session_models import SessionModel
from sqlsymphony_orm.models.session_models import SQLiteSession
from pyechonext.middleware import middlewares


settings = Settings(
	BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates", SECRET_KEY="secret"
)
echonext = EchoNext(
	__name__, settings, middlewares, application_type=ApplicationType.HTML
)
session = SQLiteSession("echonext.db")


class User(SessionModel):
	__tablename__ = "Users"

	id = IntegerField(primary_key=True)
	name = TextField(null=False)
	cash = RealField(null=False, default=0.0)

	def __repr__(self):
		return f"<User {self.pk}>"


@echonext.route_page("/")
def home(request, response):
	user = User(name="John", cash=100.0)
	session.add(user)
	session.commit()
	return "Hello from the HOME page"


@echonext.route_page("/users")
def about(request, response):
	users = session.get_all_by_model(User)

	return f"Users: {[f'{user.name}: {user.cash}$' for user in users]}"
```

---

Таким образом у нас получился почти полноценный фреймворк на Python. Пока ему не хватает:

 + Аутентификация
 + Вебсокеты
 + Интеграция celery
 + Кэширование
 + Статичные файлы

Если вам понравилась статья, я могу написать вторую часть, где мы реализуем еще больше функционала.

# Заключение
Это один из моих самых больших и проработанных проектов. Это было сложно, но интересно. Я лучше разобрался в структуре веб-приложений и фреймворков.

Если у вас есть вопросы или предложения, пишите в комментарии, рад буду выслушать.

Репозиторий исходного кода доступен по [ссылке](https://github.com/alexeev-prog/pyEchoNext).

Буду рад, если вы присоединитесь к моему небольшому [телеграм-блогу](https://t.me/hex_warehouse). Анонсы статей, новости из мира IT и полезные материалы для изучения программирования и смежных областей. Не бейте :)

