from dataclasses import dataclass
from typing import Type

from pyechonext.views import IndexView, View


@dataclass
class URL:
	"""
	This dataclass describes an url.
	"""

	url: str
	view: Type[View]


url_patterns = [URL(url="/", view=IndexView)]
