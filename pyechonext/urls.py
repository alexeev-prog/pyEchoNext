from dataclasses import dataclass
from typing import Type
from pyechonext.views import View, IndexView


@dataclass
class URL:
	url: str
	view: Type[View]


url_patterns = [URL(url="", view=IndexView)]
