from dataclasses import dataclass
from typing import Optional, Type

from pyechonext.mvc.controllers import PageController


@dataclass
class URL:
    """
    This dataclass describes an url.
    """

    path: str
    controller: Type[PageController]
    summary: Optional[str] = None


url_patterns = []
