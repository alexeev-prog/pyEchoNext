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
poetry add ruff loguru pysocks fire python-dotenv jinja2 parse gunicorn
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

# 
