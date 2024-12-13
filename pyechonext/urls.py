from dataclasses import dataclass
from typing import Type

from pyechonext.mvc.controllers import PageController


@dataclass
class URL:
	"""
	This dataclass describes an url.
	"""

	path: str
	controller: Type[PageController]


url_patterns = []
