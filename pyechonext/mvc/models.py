from abc import ABC, abstractmethod
from typing import Any, Union

from pyechonext.request import Request
from pyechonext.response import Response


class BaseModel(ABC):
    """
    This class describes a base model.
    """

    @abstractmethod
    def get_response(self, *args, **kwargs) -> Response:
        """
        Creates a response.

        :param		args:	 The arguments
        :type		args:	 list
        :param		kwargs:	 The keywords arguments
        :type		kwargs:	 dictionary

        :returns:	response object
        :rtype:		Response
        """
        raise NotImplementedError

    @abstractmethod
    def get_request(self, *args, **kwargs) -> Request:
        """
        Creates a request.

        :param		args:	 The arguments
        :type		args:	 list
        :param		kwargs:	 The keywords arguments
        :type		kwargs:	 dictionary

        :returns:	request object
        :rtype:		Request
        """
        raise NotImplementedError


class PageModel(BaseModel):
    """
    This class describes a page model.
    """

    def __init__(self, request: Request = None, response: Response = None):
        """
        Constructs a new instance.

        :param		request:   The request
        :type		request:   Request
        :param		response:  The response
        :type		response:  Response
        """
        self.request = request
        self.response = response

    def get_response(
        self, data: Union[Response, Any], app, *args, **kwargs
    ) -> Response:
        """
        Creates a response.

        :param		args:	 The arguments
        :type		args:	 list
        :param		kwargs:	 The keywords arguments
        :type		kwargs:	 dictionary

        :returns:	response object
        :rtype:		Response
        """

        if isinstance(data, Response):
            response = data
        else:
            response = Response(body=str(data), *args, **kwargs)

        if response.use_i18n:
            response.body = app.i18n_loader.get_string(response.body)

        response.body = app.get_and_save_cache_item(response.body, response.body)

        return response

    def get_request(self, *args, **kwargs) -> Request:
        """
        Creates a request.

        :param		args:	 The arguments
        :type		args:	 list
        :param		kwargs:	 The keywords arguments
        :type		kwargs:	 dictionary

        :returns:	request object
        :rtype:		Request
        """
        return Request(*args, **kwargs)
