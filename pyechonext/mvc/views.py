from abc import ABC, abstractmethod
from typing import Union, Any, Optional
from pyechonext.response import Response
from pyechonext.request import Request
from pyechonext.i18n_l10n import JSONi18nLoader


class BaseView(ABC):
	@abstractmethod
	def render(self, request: Request, response: Response, *args, **kwargs):
		raise NotImplementedError


class i18nView(BaseView):
	def render(self, data: str, i18n_loader: JSONi18nLoader, **kwargs):
		return i18n_loader.get_string(data, **kwargs)


class PageView(BaseView):
	def render(self, data: Union[Response, Any], *args, **kwargs):
		if self.use_i18n:
			data = self.i18n_loader.get_string(data)

		if isinstance(data, Response):
			return data
		else:
			response = Response(body=str(data), *args, **kwargs)
			return response
