from abc import ABC, abstractmethod
from typing import Any, Optional, Union

from pyechonext.request import Request
from pyechonext.response import Response


class BaseModel(ABC):
    """
    This class describes a base model.
    """

    @abstractmethod
    def get_response(self, *args, **kwargs) -> Response:
        """Create a Response object

        Raises:
            NotImplementedError: abstract method

        Returns:
            Response: response object
        """
        raise NotImplementedError

    @abstractmethod
    def get_request(self, *args, **kwargs) -> Request:
        """Create a Request object

        Raises:
            NotImplementedError: abstract method

        Returns:
            Request: request object
        """
        raise NotImplementedError


class PageModel(BaseModel):
    """
    This class describes a page model.
    """

    def __init__(
        self, request: Optional[Request] = None, response: Optional[Response] = None
    ):
        """Initializie a Page Model

        Args:
            request (Request, optional): request object. Defaults to None.
            response (Response, optional): response object. Defaults to None.
        """
        self.request = request
        self.response = response

    def get_response(self, data: Union[Response, Any], *args, **kwargs) -> Response:
        """Get a response

        Args:
            data (Union[Response, Any]): response object or any data

        Returns:
            Response: response object
        """

        if isinstance(data, Response):
            response = data
        else:
            response = Response(body=str(data), *args, **kwargs)

        return response

    def get_request(self, *args, **kwargs) -> Request:
        """Create a request

        Returns:
            Request: request object
        """
        return Request(*args, **kwargs)
