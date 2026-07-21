from abc import ABC, abstractmethod

from pyechonext.mvc.models import PageModel


class BaseView(ABC):
    """
    Base visualization of the data that model contains.
    """

    @abstractmethod
    def render(self, model: PageModel) -> str | dict:
        """Render the given model

        Args:
            model (PageModel): model for render

        Returns:
            str: rendered content
        """
        raise NotImplementedError


class PageView(BaseView):
    """
    Page visualization of the data that model contains.
    """

    def render(self, model: PageModel) -> str | dict:
        """Render the given model

        Args:
            model (PageModel): model for render

        Returns:
            str: rendered content
        """
        return model.response.body
