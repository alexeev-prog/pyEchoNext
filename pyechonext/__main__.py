import os
import fire
from rich import print


MAIN_APP_TEMPLATE = '''
import os
from pyechonext.utils.exceptions import MethodNotAllow
from pyechonext.app import ApplicationType, EchoNext
from pyechonext.urls import URL
from pyechonext.config import Settings
from pyechonext.template_engine.builtin import render_template
from pyechonext.middleware import middlewares

from views import IndexView


url_patterns = [URL(url="/", view=IndexView)]
settings = Settings(
	BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"
)
echonext = EchoNext(
	{{APPNAME}}, settings, middlewares, urls=url_patterns, application_type=ApplicationType.HTML
)
'''

INDEX_VIEW_TEMPLATE = '''
from pyechonext.views import View


class IndexView(View):
	def get(self, request, response, **kwargs):
		return 'Hello World!'

	def post(self, request, response, **kwargs):
		raise MethodNotAllow(f'Request {request.path}: method not allow')
'''


class ProjectCreator:
	"""
	This class describes a project creator.
	"""

	def __init__(self, appname: str):
		"""
		Constructs a new instance.

		:param		appname:	   The appname
		:type		appname:	   str
		:param		project_dirs:  The project dirs
		:type		project_dirs:  list
		"""
		self.appname = appname
		self.base_dir = appname
		self.project_dirs = ['templates', 'views']
		os.makedirs(self.base_dir, exist_ok=True)

	def _create_projects_dirs(self):
		"""
		Creates projects dirs.
		"""
		for project_dir in self.project_dirs:
			print(f'[cyan]Make dir: {project_dir}[/cyan]')
			os.makedirs(os.path.join(self.base_dir, project_dir), exist_ok=True)

	def _create_projects_files(self):
		"""
		Creates projects files.
		"""
		with open(os.path.join(self.base_dir, 'README.md'))
			file.write(f'# {self.appname}\nMade with love by [pyEchoNext](https://github.com/alexeev-prog/pyEchoNext)')

	def _create_index_view(self):
		"""
		Creates an index view.
		"""
		with open(os.path.join(self.base_dir, 'views/main.py'), 'w') as file:
			file.write(INDEX_VIEW_TEMPLATE)

		with open(os.path.join(self.base_dir, 'views/__init__.py'), 'w') as file:
			file.write('from views.main import IndexView\nall=("IndexView",)')

	def _create_main_file(self):
		"""
		Creates a main file.
		"""
		with open(os.path.join(self.base_dir, f'{self.appname}.py'), 'w') as file:
			file.write(MAIN_APP_TEMPLATE.replace("'{{APPNAME}}'", self.appname))

	def build(self):
		"""
		Build project
		"""
		print(f'[bold]Start build project architecture: {self.appname}[/bold]')
		print(f'[blue]Create dirs...[/blue]')
		self._create_projects_dirs()
		print(f'[blue]Create project files...[/blue]')
		self._create_projects_files()
		print(f'[blue]Create index view...[/blue]')
		self._create_index_view()
		print(f'[blue]Create main file...[/blue]')
		self._create_main_file()
		print(f'[green]Successfully builded![/green]')


def build_app(name: str = 'webapp'):
	"""
	Builds an application.

	:param		name:  The name
	:type		name:  str
	"""
	creator = ProjectCreator(name)
	creator.build()


fire.Fire(build_app)
