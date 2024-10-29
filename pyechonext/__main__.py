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

from views import IndexView


url_patterns = [URL(url="/", view=IndexView)]
settings = Settings(
	BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"
)
echonext = EchoNext(
	{{APPNAME}}, settings, urls=url_patterns, application_type=ApplicationType.HTML
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

		:param      appname:       The appname
		:type       appname:       str
		:param      project_dirs:  The project dirs
		:type       project_dirs:  list
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
			os.makedirs(os.path.join(self.base_dir, project_dir), exist_ok=True)

	def _create_index_view(self):
		with open(os.path.join(self.base_dir, 'views/main.py'), 'w') as file:
			file.write(INDEX_VIEW_TEMPLATE)

		with open(os.path.join(self.base_dir, 'views/__init__.py'), 'w') as file:
			file.write('from views.main import IndexView\nall=("IndexView",)')

	def _create_main_file(self):
		with open(os.path.join(self.base_dir, f'{self.appname}.py'), 'w') as file:
			file.write(MAIN_APP_TEMPLATE.replace("'{{APPNAME}}'", self.appname))

	def build(self):
		print(f'[cyan]Create dirs...[/cyan]')
		self._create_projects_dirs()
		print(f'[cyan]Create index view...[/cyan]')
		self._create_index_view()
		print(f'[cyan]Create main file...[/cyan]')
		self._create_main_file()


def build_app(name: str = 'webapp'):
	"""
	Builds an application.

	:param      name:  The name
	:type       name:  str
	"""
	creator = ProjectCreator(name)
	creator.build()


fire.Fire(build_app)
