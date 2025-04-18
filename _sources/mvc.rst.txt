MVC Architecture
=============================

MVC stands for Model-View-Controller, an architectural pattern that divides an application into three logical components: the model, the view, and the controller.

The main idea of the MVC pattern is that each section of code has its own purpose. Part of the code contains application data, the other is responsible for how the user sees it, the latter controls its operation.

- Model: The model stores data and associated logic, and anchors the structure of the application. This is where the core data resides, along with the business rules that govern how that data can be created, read, updated, or deleted. The model is usually designed to notify the view of any changes that need to be reflected in the user interface. For instance, if a new record is added, the model could trigger an update to the view to reflect that change.

- View: The view consists of functions that are responsible for the interface and how the user interacts with it. Views are created based on data collected from the model, and they determine how that data is presented to the user. A good view handles the display logic and can be designed to update dynamically as the underlying data changes. It should be decoupled from the model, meaning that it should not need to know the details of how data is managed or stored.

- Controller: The controller links the model and view. It acts as an intermediary that processes user input received from the view, interacts with the model to update the application's state, and then returns the output to the view. For example, if a user submits a form, the controller will gather that input, validate it, and often pass it to the model for further action, such as saving it in a database or retrieving related data. 

In summary, the MVC pattern promotes organized code and separation of concerns, making it easier to manage and maintain complex applications. By clearly delineating responsibilities among the model, view, and controller, developers can work on individual components without affecting others, leading to better collaboration and more scalable solutions. This architectural design is widely adopted in various programming languages and frameworks, enabling developers to build robust and efficient software applications.

Source code available at `this link <https://github.com/alexeev-prog/pyEchoNext/tree/main/pyechonext/mvc>`__.

Controllers
-----------

Here is source code of Controllers.

.. code:: python

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

Models
------

Here is source code of Models.

.. code:: python

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

			:param		request:    The request
			:type		request:    Request
			:param		response:  The response
			:type		response:  Response
			"""
			self.request = request
			self.response = response

		def get_response(
			self, data: Union[Response, Any], app: EchoNext, *args, **kwargs
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

Views
-----

Here is source code of Views.

.. code:: python

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

Simple Example
--------------

Here is simple example of API with PageControllers:

.. code::python

	import os

	from pyechonext.app import ApplicationType, EchoNext
	from pyechonext.config import Settings
	from pyechonext.middleware import middlewares
	from pyechonext.mvc.controllers import PageController
	from pyechonext.response import Response
	from pyechonext.urls import URL


	class UsersPageController(PageController):
		def get(self, request, response, **kwargs):
			return Response(request, body={"users": "get"})

		def post(self, request, response, **kwargs):
			return {"users": "post"}


	url_patterns = [URL(path="/users", controller=UsersPageController)]

	settings = Settings(
		BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"
	)

	echonext = EchoNext(
		__name__,
		settings,
		middlewares,
		urls=url_patterns,
		application_type=ApplicationType.JSON,
	)


	@echonext.route_page("/book")
	class BooksResource(PageController):
		def get(self, request, response, **kwargs):
			return {"params": request.GET, "page": "books"}

		def post(self, request, response, **kwargs):
			return {"params": request.POST, "page": "books"}
