from abc import ABC, abstractmethod
from urllib.parse import parse_qs
from uuid import uuid4

from pyechonext.logging import logger
from pyechonext.request import Request
from pyechonext.response import Response
from pyechonext.utils.exceptions import WebError, pyEchoNextException


class BaseMiddleware(ABC):
    """
    This abstract class describes a base middleware.
    """

    @abstractmethod
    def to_request(self, request: Request):
        """Apply actions to request

        Args:
           request (Request): request object

        Raises:
           NotImplementedError: abstract method
        """
        raise NotImplementedError

    @abstractmethod
    def to_response(self, response: Response):
        """Apply actions to response

        Args:
            response (Response): response object

        Raises:
           NotImplementedError: abstract method
        """
        raise NotImplementedError

    @abstractmethod
    def process_template(self, *args, **kwargs):
        """Process template with middleware

        Raises:
            NotImplementedError: abstract method
        """
        raise NotImplementedError

    @abstractmethod
    def process_exception(self, exception: Exception):
        """Process exception with middleware

        Args:
           exception (Exception): exception class

        Raises:
           exception: exception from arguments
        """
        raise NotImplementedError


class SessionMiddleware(BaseMiddleware):
    """
    This class describes a session (cookie) middleware.
    """

    def to_request(self, request: Request):
        """Apply cookies to request

        Args:
            request (Request): request object
        """
        cookie = request.environ.get("HTTP_COOKIE", None)

        if not cookie:
            return

        session_id = parse_qs(cookie)["session_id"][0]
        logger.debug(
            f"Set session_id={session_id} for request {request.method} {request.path}"
        )
        request.extra["session_id"] = session_id

    def to_response(self, response: Response):
        """Get session uuid by response

        Args:
            response (Response): response
        """
        if not response.request.session_id:
            session_id = uuid4()
            logger.debug(
                f"Set session_id={session_id} for response"
                f" {response.status_code} {response.request.path}"
            )
            response.add_headers([
                ("Set-Cookie", f"session_id={session_id}"),
            ])

    def process_template(self, *args, **kwargs):
        """Process template with middleware

        Raises:
            NotImplementedError: abstract method
        """
        raise NotImplementedError

    def process_exception(self, exception: Exception):
        """Process exception with middleware

        Args:
            exception (Exception): exception class

        Raises:
            exception: exception from arguments
        """
        if not isinstance(exception, pyEchoNextException) or not isinstance(
            exception, WebError
        ):
            raise exception


middlewares = [SessionMiddleware]
