from os.path import join, exists, getmtime
from jinja2 import BaseLoader, TemplateNotFound
from jinja2 import Environment, select_autoescape
from loguru import logger
from pyechonext.request import Request


class TemplateLoader(BaseLoader):
	"""
	This class describes a jinja2 template loader.
	"""

	def __init__(self, path: str):
		"""
		Constructs a new instance.

		:param		path:  The path
		:type		path:  str
		"""
		self.path = path

	def get_source(self, environment, template):
		path = join(self.path, template)

		if not exists(path):
			raise TemplateNotFound(template)

		mtime = getmtime(path)

		with open(path) as f:
			source = f.read()

		return source, path, lambda: mtime == getmtime(path)


class TemplateEngine:
	"""
	This class describes a jinja template engine.
	"""

	def __init__(self, base_dir: str, templates_dir: str):
		"""
		Constructs a new instance.

		:param		base_dir:		The base dir
		:type		base_dir:		str
		:param		templates_dir:	The templates dir
		:type		templates_dir:	str
		"""
		self.base_dir = base_dir
		self.templates_dir = join(base_dir, templates_dir)
		self.env = Environment(
			loader=TemplateLoader(self.templates_dir), autoescape=select_autoescape()
		)

	def build(self, template_name: str, **kwargs):
		template = self.env.get_template(template_name)

		return template.render(**kwargs)


def render_template(request: Request, template_name: str, **kwargs) -> str:
	"""
	Render template

	:param		request:		 The request
	:type		request:		 Request
	:param		template_name:	 The template name
	:type		template_name:	 str
	:param		kwargs:			 The keywords arguments
	:type		kwargs:			 dictionary

	:returns:	raw template string
	:rtype:		str

	:raises		AssertionError:	 BASE_DIR and TEMPLATES_DIR is empty
	"""
	assert request.settings.BASE_DIR
	assert request.settings.TEMPLATES_DIR

	engine = TemplateEngine(request.settings.BASE_DIR, request.settings.TEMPLATES_DIR)

	logger.debug(f"Jinja2 template engine: render {template_name} ({request.path})")

	return engine.build(template_name, **kwargs)
