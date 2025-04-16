 # pyEchoNext / Генерация онлайн-документации

---

pyEchoNext позволяет генерировать онлайн документацию:

```python
from pyechonext.apidoc_ui import APIDocumentation, APIDocUI

echonext = EchoNext(
	... # params here
)
apidoc = APIDocumentation(echonext)


@echonext.route_page('/api-docs')
def api_docs(request, response):
	ui = APIDocUI(apidoc.generate_spec())
	return ui.generate_html_page()
```

---

[Содержание](./index.md)

