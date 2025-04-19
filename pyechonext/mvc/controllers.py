from abc import ABC, abstractmethod
from typing import Any, Union

from pyechonext.mvc.models import PageModel
from pyechonext.mvc.views import PageView
from pyechonext.request import Request
from pyechonext.response import Response
from pyechonext.utils.exceptions import MethodNotAllow


class BaseController(ABC):
    """
    Controls the data flow into a base object and updates the view whenever data changes.
    """

    @abstractmethod
    def get(self, request: Request, response: Response, *args, **kwargs):
        """
        Get method

        :param		request:			  The request
        :type		request:			  Request
        :param		response:			  The response
        :type		response:			  Response
        :param		args:				  The arguments
        :type		args:				  list
        :param		kwargs:				  The keywords arguments
        :type		kwargs:				  dictionary

        :raises		NotImplementedError:  abstract method
        """
        raise NotImplementedError()

    @abstractmethod
    def post(self, request: Request, response: Response, *args, **kwargs):
        """
        Post method

        :param		request:			  The request
        :type		request:			  Request
        :param		response:			  The response
        :type		response:			  Response
        :param		args:				  The arguments
        :type		args:				  list
        :param		kwargs:				  The keywords arguments
        :type		kwargs:				  dictionary

        :raises		NotImplementedError:  abstract method
        """
        raise NotImplementedError()


class PageController(BaseController):
    """
    Controls the data flow into a page object and updates the view whenever data changes.
    """

    def _create_model(
        self, request: Request, data: Union[Response, Any], app: "EchoNext"
    ) -> PageModel:
        """
        Creates a model.

        :param		request:  The request
        :type		request:  Request
        :param		data:	  The data
        :type		data:	  Union[Response, Any]
        :param		app:	  The application
        :type		app:	  EchoNext

        :returns:	The page model.
        :rtype:		PageModel
        """
        model = PageModel(request)
        model.response = model.get_response(data, app)

        return model

    def get_rendered_view(
        self, request: Request, data: Union[Response, Any], app: "EchoNext"
    ) -> str:
        """
        Gets the rendered view.

        :param		request:  The request
        :type		request:  Request
        :param		data:	  The data
        :type		data:	  Union[Response, Any]
        :param		app:	  The application
        :type		app:	  EchoNext

        :returns:	The rendered view.
        :rtype:		str
        """
        model = self._create_model(request, data, app)

        view = PageView()

        return view.render(model)

    def get(self, request: Request, response: Response, *args, **kwargs):
        """
        Get Method

        :param		request:		 The request
        :type		request:		 Request
        :param		response:		 The response
        :type		response:		 Response
        :param		args:			 The arguments
        :type		args:			 list
        :param		kwargs:			 The keywords arguments
        :type		kwargs:			 dictionary

        :raises		MethodNotAllow:	 get method not allowed
        """
        raise MethodNotAllow("Method Not Allow: GET")

    def post(self, request: Request, response: Response, *args, **kwargs):
        """
        Post Method

        :param		request:		 The request
        :type		request:		 Request
        :param		response:		 The response
        :type		response:		 Response
        :param		args:			 The arguments
        :type		args:			 list
        :param		kwargs:			 The keywords arguments
        :type		kwargs:			 dictionary

        :raises		MethodNotAllow:	 post method not allowed
        """
        raise MethodNotAllow("Method Not Allow: Post")
