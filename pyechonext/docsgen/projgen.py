from typing import Callable, Any
from pyechonext.app import EchoNext
from pyechonext.docsgen.document import (
	InitiationSection,
	DocumentFolder,
	ProjectManager,
	ProjectTemplate,
	RoutesSubsection,
	DocumentSection,
)


class ProjDocumentation:
	"""
	This class describes an api documentation.
	"""

	def __init__(self, echonext_app: EchoNext):
		"""
		Constructs a new instance.

		:param		echonext_app:  The echonext application
		:type		echonext_app:  EchoNext
		"""
		self.app = echonext_app
		self.app_name = echonext_app.app_name
		self.pages = {}

	def generate_documentation(self):
		"""
		Generate documentation
		"""
		section = self._generate_introduction()
		self._generate_subsections(section)
		folder = DocumentFolder(
			"api",
			f"{self.app_name}/docs",
			[
				section,
			],
		)

		project_manager = ProjectManager(
			f"{self.app_name}",
			"Project Web Application",
			"Project application based on pyEchoNext web-framework",
			f"{self.app_name}",
			f"{self.app_name}",
			f"{self.app_name}",
			ProjectTemplate.BASE,
			[folder],
			[section],
		)

		project_manager.process_project()

	def _generate_introduction(self) -> InitiationSection:
		"""
		Generate introduction

		:returns:	The initiation section.
		:rtype:		InitiationSection
		"""
		section = InitiationSection(
			f"Project {self.app_name}",
			f"Project Documentation for {self.app_name}",
			{"Routes": ", ".join(self.app.routes.keys())},
		)
		return section

	def _generate_subsections(self, section: DocumentSection):
		"""
		Generate subsections

		:param		section:  The section
		:type		section:  DocumentSection
		"""
		subsections = []

		for path, data in self.pages.items():
			subsections.append(
				RoutesSubsection(
					path,
					{
						"Route": f'Methods: {data["methods"]}\n\nReturn type: {data["return_type"]}',
						"Extra": f'Extra: {"\n".join([f" + {key}: {value}" for key, value in data["extra"].items()])}',
					},
					section,
				)
			)

		for subsection in subsections:
			section.link_new_subsection(subsection)

	def documentate_route(
		self,
		page_path: str,
		return_type: Any,
		params: dict,
		methods: list,
		extra: dict = {},
	) -> Callable:
		"""
		Add routed page to documentation

		:param		page_path:	  The page path
		:type		page_path:	  str
		:param		return_type:  The return type
		:type		return_type:  Any
		:param		params:		  The parameters
		:type		params:		  dict
		:param		methods:	  The methods
		:type		methods:	  list
		:param		extra:		  The extra
		:type		extra:		  dict

		:returns:	wrapper handler
		:rtype:		Callable
		"""
		if page_path in self.pages:
			return

		def wrapper(handler):
			"""
			Wrapper for handler

			:param		handler:  The handler
			:type		handler:  callable

			:returns:	handler
			:rtype:		callable
			"""
			self.pages[page_path] = {
				"page_path": page_path,
				"doc": handler.__doc__,
				"funcname": handler.__name__,
				"return_type": return_type,
				"params": params,
				"methods": methods,
				"extra": extra,
			}
			return handler

		return wrapper
