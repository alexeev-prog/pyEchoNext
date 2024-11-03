import os
from abc import ABC
from enum import Enum
from typing import List, Dict, Any
from loguru import logger

from pyechonext.utils import get_current_datetime


class DocumentSubsection(ABC):
	"""
	This class describes a document subsection.
	"""

	def __init__(
		self, title: str, content: Dict[str, Any], main_section: "DocumentSection"
	):
		"""
		Constructs a new instance.

		:param		title:		   The title
		:type		title:		   str
		:param		content:	   The content
		:type		content:	   str
		:param		main_section:  The main section
		:type		main_section:  DocumentSection
		"""
		self.title = title
		self.content = content
		self.main_section = main_section
		self.creation_date = get_current_datetime()

	def set_new_main_section(self, new_main_section: "DocumentSection"):
		"""
		Sets the new main section.

		:param		new_main_section:  The new main section
		:type		new_main_section:  DocumentSection
		"""
		logger.debug(f'Set new section for subsection "{self.title}"')
		self.main_section = new_main_section


class DocumentSection(ABC):
	"""
	This abstract metaclass describes a documentation section.
	"""

	def __init__(self, title: str, introduction: str, content: Dict[str, Any]):
		"""
		Constructs a new instance.

		:param		title:		   The title
		:type		title:		   str
		:param		introduction:  The introduction
		:type		introduction:  str
		:param		content:	   The content
		:type		content:	   { type_description }
		"""
		self.title = title
		self.introduction = introduction
		self.content = content
		self.linked_sections = {}
		self.linked_subsections = {}
		self.creation_date = get_current_datetime()
		self.modification_date = self.creation_date

	def link_new_subsection(self, linked_subsection: DocumentSubsection):
		"""
		Links a new subsection.

		:param		linked_subsection:	The linked subsection
		:type		linked_subsection:	DocumentSubsection
		"""

		self.linked_subsections[linked_subsection.title] = linked_subsection
		linked_subsection.set_new_main_section(self)
		logger.info(f'Linked new subsection: "{linked_subsection.title}"')

	def link_new_section(self, linked_section: "DocumentSection"):
		"""
		Links a new section.

		:param		linked_section:	 The linked section
		:type		linked_section:	 DocumentSection
		"""
		self.linked_sections[linked_section.title] = linked_section
		self.linked_section.link_new_section(self)
		logger.info(f"Linked new section: {linked_section.title}")

	def get_filename(self) -> str:
		"""
		Gets the filename.

		:returns:	The filename.
		:rtype:		str
		"""
		return f'{self.title.replace(" ", "_")}.md'

	def modify_title(self, new_title: str):
		"""
		Modify section title

		:param		new_title:	The new title
		:type		new_title:	str
		"""
		logger.debug(f"Title modified: {self.title} -> {new_title}")
		self.title = new_title
		self.modification_date = get_current_datetime()

	def modify_description(self, new_description: str):
		"""
		Modify section description

		:param		new_description:  The new description
		:type		new_description:  str
		"""
		logger.debug(f"Description modified: {self.description} -> {new_description}")
		self.description = new_description
		self.modification_date = get_current_datetime()

	def modify_content(self, new_content: Dict[str, Any]):
		"""
		Modify section content

		:param		new_content:  The new content
		:type		new_content:  Dict[str, Any]
		"""
		logger.debug(f"Content modified: {self.content} -> {new_content}")
		self.content = new_content
		self.modification_date = get_current_datetime()

	def get_markdown_page(self) -> List[str]:
		"""
		Gets the page in markdown formatting

		:returns:	The markdown page.
		:rtype:		List[str]
		"""
		logger.debug(f"Generating document section [{self.title}]...")
		page = [f"# {self.title}"]
		page.append(f"{self.introduction}\n")
		page.append(
			f" + *Creation date*: {self.creation_date}\n + *Modification date*: {self.modification_date}\n"
		)

		for key, value in self.content.items():
			page.append(f"## {key}\n{value}\n")

		if len(self.linked_subsections) > 0:
			page.append("---\n")
			page.append("## Subsections\n")

			for title, subsection in self.linked_subsections.items():
				page.append(f"### {title}")
				page.append(f"Creation date: {subsection.creation_date}\n")
				for key, value in subsection.content.items():
					page.append(f"#### {key}\n{value}\n")

		page.append("---\n")
		page.append("Created by [JustProj](https://github.com/alexeev-prog/JustProj)")

		logger.info(f"Document section [{self.title}] successfully generated!")

		return page


class RoutesSubsection(DocumentSubsection):
	"""
	This class describes a routes section.
	"""

	def __init__(
		self, title: str, content: Dict[str, Any], main_section: "DocumentSection"
	):
		"""
		Constructs a new instance.

		:param		title:		   The title
		:type		title:		   str
		:param		content:	   The content
		:type		content:	   str
		:param		main_section:  The main section
		:type		main_section:  DocumentSection
		"""
		self.title = title
		self.content = content
		self.main_section = main_section
		self.creation_date = get_current_datetime()


class InitiationSection(DocumentSection):
	"""
	This class describes an initiation section.
	"""

	def __init__(self, title: str, introduction: str, content: Dict[str, Any]):
		"""
		Constructs a new instance.

		:param		title:		   The title
		:type		title:		   str
		:param		introduction:  The introduction
		:type		introduction:  str
		:param		content:	   The content
		:type		content:	   Dict[str, Any]
		"""
		self.title = f"Initiation-{title}"
		self.introduction = introduction
		self.content = content
		self.linked_sections = {}
		self.linked_subsections = {}
		self.creation_date = get_current_datetime()
		self.modification_date = self.creation_date


class DocumentFolder:
	"""
	This class describes a document folder.
	"""

	def __init__(
		self, name: str, project_root_dir: str, sections: List[DocumentSection]
	):
		"""
		Constructs a new instance.

		:param		name:			   The name
		:type		name:			   str
		:param		project_root_dir:  The project root dir
		:type		project_root_dir:  str
		:param		sections:		   The sections
		:type		sections:		   List[DocumentSection]
		"""
		self.name = name.replace(" ", "_")
		self.project_root_dir = project_root_dir
		os.makedirs(self.project_root_dir, exist_ok=True)
		self.folderpath = os.path.join(self.project_root_dir, self.name)
		os.makedirs(self.folderpath, exist_ok=True)
		self.sections = sections

		self._create_index_file()

	def _create_index_file(self):
		"""
		Creates an index file.
		"""
		with open(os.path.join(self.folderpath, "index.md"), "w") as file:
			file.write(f"# {self.name}\n\n")

			for section in self.sections:
				file.write(f"## {section.title}\n{section.introduction}\n")


class DocumentManager:
	"""
	This class describes a document manager.
	"""

	def __init__(
		self,
		project_name: str,
		short_project_introduction: str,
		project_description: str,
		repo_author: str,
		repo_name: str,
		project_root_dir: str,
		folders: List[DocumentFolder],
	):
		"""
		Constructs a new instance.

		:param		project_name:		  The project name
		:type		project_name:		  str
		:param		project_description:  The project description
		:type		project_description:  str
		:param		project_root_dir:	  The project root dir
		:type		project_root_dir:	  str
		:param		folders:			  The folders
		:type		folders:			  List[DocumentFolder]
		"""
		self.project_name = project_name
		self.short_project_introduction = short_project_introduction
		self.project_description = project_description
		self.project_root_dir = project_root_dir
		self.folders = folders
		self.repo_author = repo_author
		self.repo_name = repo_name

		os.makedirs(self.project_root_dir, exist_ok=True)

	def generate_readme(self):
		"""
		Generate readme file
		"""
		logger.debug("Generate README...")
		page = f"""# {self.repo_name}

<p align="center">{self.short_project_introduction}</p>
<br>
<p align="center">
	<img src="https://img.shields.io/github/languages/top/{self.repo_author}/{self.repo_name}?style=for-the-badge">
	<img src="https://img.shields.io/github/languages/count/{self.repo_author}/{self.repo_name}?style=for-the-badge">
	<img src="https://img.shields.io/github/license/{self.repo_author}/{self.repo_name}?style=for-the-badge">
	<img src="https://img.shields.io/github/stars/{self.repo_author}/{self.repo_name}?style=for-the-badge">
	<img src="https://img.shields.io/github/issues/{self.repo_author}/{self.repo_name}?style=for-the-badge">
	<img src="https://img.shields.io/github/last-commit/{self.repo_author}/{self.repo_name}?style=for-the-badge">
</p>

{self.project_description}

## Folders
DocumentFolders (is not directories):\n
"""
		for folder in self.folders:
			page += f"### {folder.name}\n"
			page += f"Path: {folder.folderpath}\n"

			for section in folder.sections:
				page += f"\n#### {section.title}\n"
				page += f"{section.introduction}\n"

				if len(section.linked_sections) > 0:
					page += "\nLinked sections:\n\n"

					for linked_section in section.linked_sections:
						page += f" + {linked_section.title}\n"

				if len(section.linked_subsections) > 0:
					page += "\nLinked subsections:\n\n"

					for linked_subsection in section.linked_subsections:
						page += f" + {linked_subsection}\n"

		with open(os.path.join(self.project_root_dir, "README.md"), "w") as file:
			file.write(page)

		logger.info("README generated successfully!")

	def generate_pages(self):
		"""
		Generate pages of sections in folders
		"""
		docs_dir = os.path.join(self.project_root_dir, "docs")
		os.makedirs(docs_dir, exist_ok=True)

		logger.debug("Generating pages...")

		for folder in self.folders:
			for section in folder.sections:
				section_filename = os.path.join(
					folder.folderpath, section.get_filename()
				)
				logger.debug(f'Generating page "{section.title}" [{section_filename}]')
				page = section.get_markdown_page()

				with open(section_filename, "w") as file:
					for line in page:
						file.write(f"{line}\n")

		logger.info("Pages successfully generated!")


class ProjectTemplate(Enum):
	BASE = 0
	CPP = 1
	PYTHON = 2


class ProjectStructureGenerator:
	"""
	This class describes a project structure generator.
	"""

	def __init__(self, project_root_dir: str, project_template: ProjectTemplate):
		"""
		Constructs a new instance.

		:param		project_root_dir:  The project root dir
		:type		project_root_dir:  str
		:param		project_template:  The project template
		:type		project_template:  ProjectTemplate
		"""
		self.project_root_dir = project_root_dir
		self.project_template = project_template
		os.makedirs(self.project_root_dir, exist_ok=True)
		self.structure = {}

	def add_directory(self, dir_name: str, dir_files: List[str]):
		"""
		Adds a directory.

		:param		dir_name:	The dir name
		:type		dir_name:	str
		:param		dir_files:	The dir files
		:type		dir_files:	List[str]
		"""
		self.structure[dir_name] = {"basic": dir_files}
		logger.info(f"Add new directory: {dir_name}")

	def generate_structure(self):
		"""
		Generate project file structure
		"""
		logger.debug("Generate structure...")
		self.structure["."] = {
			"basic": [
				"README.md",
				"LICENSE",
				"BUILDING.md",
				"CHANGELOG.md",
				"CODE_OF_CONDUCT.md",
				"CONTRIBUTING.md",
				"HACKING.md",
				"SECURITY.md",
			],
		}

		if self.project_template == ProjectTemplate.CPP:
			files = [
				"CMakeLists.txt",
				"CMakeUserPresets.json",
				"CMakePresets.json",
				"conanfile.py",
				".clang-format",
				".clang-tidy",
				".clangd",
			]

			for file in files:
				self.structure["."]["basic"].append(file)
		elif self.project_template == ProjectTemplate.PYTHON:
			files = ["pyproject.toml", "requirements.txt"]

			for file in files:
				self.structure["."]["basic"].append(file)

		for directory, content in self.structure.items():
			logger.debug(
				f'[Structor Generator] Create files in directory "{directory}"'
			)

			if directory != ".":
				current_dir = os.path.join(self.project_root_dir, directory)
				os.makedirs(
					os.path.join(self.project_root_dir, directory), exist_ok=True
				)
			else:
				current_dir = self.project_root_dir

			for file in content["basic"]:
				logger.debug(f"[Structor Generator] {file} processing...")
				with open(os.path.join(current_dir, file), "w") as f:
					f.write(f"# {file}\n")

		logger.info("Structure generated successfully!")


class ProjectManager:
	"""
	This class describes a project manager.
	"""

	def __init__(
		self,
		project_name: str,
		short_project_introduction: str,
		project_description: str,
		repo_author: str,
		repo_name: str,
		project_root_dir: str,
		project_template: ProjectTemplate,
		folders: List[DocumentFolder],
		sections: List[DocumentSection],
		github: bool = True,
	):
		"""
		Constructs a new instance.

		:param		project_name:		  The project name
		:type		project_name:		  str
		:param		project_description:  The project description
		:type		project_description:  str
		:param		repo_author:		  The repo author
		:type		repo_author:		  str
		:param		repo_name:			  The repo name
		:type		repo_name:			  str
		:param		project_root_dir:	  The project root dir
		:type		project_root_dir:	  str
		:param		project_template:	  The project template
		:type		project_template:	  ProjectTemplate
		:param		folders:			  The folders
		:type		folders:			  List[DocumentFolder]
		:param		sections:			  The sections
		:type		sections:			  List[DocumentSection]
		"""
		self.project_root_dir = project_root_dir
		self.project_name = project_name
		self.project_description = project_description
		self.short_project_introduction = short_project_introduction
		self.repo_author = repo_author
		self.repo_name = repo_name
		self.project_template = project_template
		self.folders = folders
		self.sections = sections
		self.is_github = github

		if self.is_github:
			self.url = f"https://github.com/{repo_author}/{repo_name}"
		else:
			logger.warning("pyechonext API support only GitHub")

		self.structure_manager = ProjectStructureGenerator(
			project_root_dir, project_template
		)
		self.document_manager = DocumentManager(
			project_name,
			short_project_introduction,
			project_description,
			repo_author,
			repo_name,
			project_root_dir,
			folders,
		)

	def add_directory_to_structure(self, dir_name: str, files: List[str]):
		"""
		Adds a directory to structure.

		:param		dir_name:  The dir name
		:type		dir_name:  str
		:param		files:	   The files
		:type		files:	   List[str]
		"""
		self.structure_manager.add_directory(dir_name, files)

	def process_project(self, skip_readme: bool = False):
		"""
		Process project creation
		"""
		logger.info(f'Process project "{self.project_name}" creation...')
		self.structure_manager.generate_structure()
		self.document_manager.generate_pages()
		if not skip_readme:
			self.document_manager.generate_readme()
		logger.info("Project created successfully!")
