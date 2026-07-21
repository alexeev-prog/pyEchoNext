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
        """Get method of route

        Args:
            request (Request): request object
            response (Response): response object

        Raises:
            NotImplementedError: abstract method
        """
        raise NotImplementedError()

    @abstractmethod
    def post(self, request: Request, response: Response, *args, **kwargs):
        """Post method of route

        Args:
            request (Request): request object
            response (Response): response object

        Raises:
            NotImplementedError: abstract method
        """
        raise NotImplementedError()


class PageController(BaseController):
    """
    Controls the data flow into a page object and updates the view whenever data changes.
    """

    def _create_model(self, request: Request, data: Union[Response, Any]) -> PageModel:
        """Create model for page controller

        Args:
            request (Request): request object
            data (Union[Response, Any]): response object or any data

        Returns:
            PageModel: page model
        """
        model = PageModel(request)
        model.response = model.get_response(data)

        return model

    def get_rendered_view(
        self, request: Request, data: Union[Response, Any]
    ) -> str | dict:
        """Get the rendered view

        Args:
            request (Request): request object
            data (Union[Response, Any]): response object or any data

        Returns:
            str | dict: rendered view
        """
        model = self._create_model(request, data)

        view = PageView()

        return view.render(model)

    def get(self, request: Request, response: Response, *args, **kwargs):
        """Get method

        Args:
            request (Request): request object
            response (Response): response object

        Raises:
            MethodNotAllow: this method not modified in child class
        """
        raise MethodNotAllow("Method Not Allow: GET")

    def post(self, request: Request, response: Response, *args, **kwargs):
        """Post method

        Args:
            request (Request): request object
            response (Response): response object

        Raises:
            MethodNotAllow: this method not modified in child class
        """
        raise MethodNotAllow("Method Not Allow: Post")
