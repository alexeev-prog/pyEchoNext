from dataclasses import dataclass
from typing import Optional

from pyechonext.mvc.controllers import PageController


@dataclass
class URL:
    """
    This dataclass describes an url.
    """

    path: str
    controller: PageController
    summary: Optional[str] = None


url_patterns = []
