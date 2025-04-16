from abc import ABC, abstractmethod

from pyechonext.mvc.models import PageModel


class BaseView(ABC):
    """
    Base visualization of the data that model contains.
    """

    @abstractmethod
    def render(self, model: PageModel):
        """
        Render data

        :param		model:	The model
        :type		model:	PageModel
        """
        raise NotImplementedError


class PageView(BaseView):
    """
    Page visualization of the data that model contains.
    """

    def render(self, model: PageModel) -> str:
        """
        Renders the given model.

        :param		model:	The model
        :type		model:	PageModel

        :returns:	model response body content
        :rtype:		str
        """
        return str(model.response.body)
