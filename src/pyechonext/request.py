import json
from typing import Any, Dict, Union
from urllib.parse import parse_qs

from pyechonext.config import Settings
from pyechonext.logging import logger


def _build_get_params_dict(raw_params: str) -> dict:
    """Build GET params dictionary

        Args:
    raw_params (str): raw params string

        Returns:
    dict: GET params
    """
    return parse_qs(raw_params)


def _build_post_params_dict(raw_params: bytes) -> dict:
    """Build POST params dictionary

        Args:
    raw_params (bytes): raw parameters

        Returns:
    dict: POST params
    """
    try:
        raw_params = json.loads(raw_params)
    except json.decoder.JSONDecodeError:
        raw_params = raw_params.decode()
    else:
        return raw_params

    return parse_qs(raw_params)


class Request:
    """
    This class describes a request.
    """

    __slots__ = (
        "environ",
        "settings",
        "method",
        "path",
        "GET",
        "POST",
        "user_agent",
        "extra",
    )

    def __init__(self, environ: dict = {}, settings: Settings = None):
        """Constructs a new request

            Args:
        environ (dict, optional): environ info. Defaults to {}.
        settings (Settings, optional): settings of app. Defaults to None.
        """
        self.environ: Dict[str, Any] = environ
        self.settings: Settings = settings
        self.method: str = self.environ.get("REQUEST_METHOD")
        self.path: str = self.environ.get("PATH_INFO")
        self.GET: Dict[Any, Any] = _build_get_params_dict(
            self.environ.get("QUERY_STRING")
        )
        self.POST: Dict[Any, Any] = _build_post_params_dict(
            self.environ.get("wsgi.input").read()
        )
        self.user_agent: str = self.environ.get("HTTP_USER_AGENT")
        self.extra: Dict[Any, Any] = {}

        logger.debug(f"New request created: {self.method} {self.path}")

    def __getattr__(self, item: Any) -> Union[Any, None]:
        """Magic method for get attrs (from extra)

            Args:
        item (Any): item key

            Returns:
        Union[Any, None]: value
        """
        return self.extra.get(item, None)
