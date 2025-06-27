import json
from ast import literal_eval
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from socks import method

from pyechonext.logging import logger
from pyechonext.request import Request
from pyechonext.security.defence import Security


class Response:
    """
    This dataclass describes a response.
    """

    __slots__ = (
        "headers",
        "status_code",
        "content_type",
        "body",
        "charset",
        "request",
        "extra",
        "_headerslist",
        "_added_headers",
    )

    default_content_type: str = "text/html"
    default_charset: str = "UTF-8"
    unicode_errors: str = "strict"
    default_conditional_response: bool = False
    default_body_encoding: str = "UTF-8"

    def __init__(
        self,
        request: Request = None,
        status_code: Optional[int] = 200,
        body: Optional[str | Dict] = None,
        headers=None,
        content_type: Optional[str] = None,
        charset: Optional[str] = None,
    ):
        """Initialize new response

        Args:
            request (Request, optional): request object. Defaults to None.
            use_i18n (bool, optional): i18n using status. Defaults to False.
            status_code (Optional[int], optional): default status code. Defaults to 200.
            body (Optional[str], optional): response body. Defaults to None.
            headers (Optional[Dict[str, str]], optional): http headers. Defaults to {}.
            content_type (Optional[str], optional): content type. Defaults to None.
            charset (Optional[str], optional): charset. Defaults to None.
            i18n_params (Optional[dict], optional): params for i18n. Defaults to {}.
        """
        if headers is None:
            headers = {}

        if status_code == 200:
            self.status_code: str = "200 OK"
        else:
            self.status_code: str = str(status_code)

        if content_type is None:
            self.content_type: str = self.default_content_type
        else:
            self.content_type: str = content_type

        if charset is None:
            self.charset: str = self.default_charset
        else:
            self.charset: str = charset

        if body is not None:
            self.body: Any = body
        else:
            self.body: str = ""

        self._headerslist: List[Any] = headers
        self._added_headers: List[Any] = []
        self.request: Request = request
        self.extra: Dict[Any, Any] = {}

        self._update_headers()

    def __getattr__(self, item: Any) -> Union[Any, None]:
        """Magic method for get attrs (from extra)

        Args:
            item (Any): item key

        Returns:
            Union[Any, None]: value
        """
        return self.extra.get(item, None)

    def _structuring_headers(self, environ: dict):
        """Structure headers

        Args:
            environ (dict): environ dictionary
        """
        headers = {
            "Host": environ.get("HTTP_HOST"),
            "Accept": environ.get("HTTP_ACCEPT"),
            "User-Agent": environ.get("HTTP_USER_AGENT"),
        }

        headers.update(Security.get_security_headers())

        for name, value in headers.items():
            self._headerslist.append((name, value))

        for header_tuple in self._added_headers:
            self._headerslist.append(header_tuple)

    def _update_headers(self) -> None:
        """Update headers by response data"""
        self._headerslist = [
            ("Content-Type", f"{self.content_type}; charset={self.charset}"),
            ("Content-Length", str(len(self.body))),
        ]

    def add_headers(self, headers: List[Tuple[str, str]]):
        """Adds new headers

        Args:
            headers (List[Tuple[str, str]]): new headers
        """
        for header in headers:
            self._added_headers.append(header)

    def _encode_body(self):
        """
        Encodes a body.
        """
        if self.content_type == "application/json":
            self.body = self.json

        try:
            self.body = self.body.encode("UTF-8")
        except AttributeError:
            self.body = str(self.body).encode("UTF-8")

    def __call__(self, environ: dict, start_response: method) -> Iterable:
        """Makes the response callable.

        This method calling another methods for encode body, fill headers and starting response.

         Args:
             environ (dict): environ data
             start_response (method): start response method

         Returns:
             Iterable: iterable encoded body
        """
        self._encode_body()

        self._update_headers()
        self._structuring_headers(environ)

        logger.debug(
            f"[{environ.get('REQUEST_METHOD')} {self.status_code}] Run response:"
            f" {self.content_type}"
        )

        start_response(status=self.status_code, headers=self._headerslist)

        return iter([self.body])

    @property
    def json(self) -> str | dict[Any, Any]:
        """Get response body as JSON

        Returns:
            dict: _description_
        """
        if self.body:
            if isinstance(self.body, str):
                try:
                    self.body = literal_eval(self.body)
                except SyntaxError:
                    return self.body

            return json.dumps(self.body)

        return {}

    def __repr__(self) -> str:
        """Returns a unambiguous string representation of the object (for debug...).

        Returns:
            str: unambiguous string representation
        """
        return f"<{self.__class__.__name__} at 0x{abs(id(self)):x} {self.status_code}>"
