from dataclasses import dataclass
from typing import Optional

from pyechonext.mvc.controllers import PageController


@dataclass(frozen=True)
class URL:
    """
    This dataclass describes an url.
    """

    path: str
    controller: PageController | type
    summary: Optional[str] = None
