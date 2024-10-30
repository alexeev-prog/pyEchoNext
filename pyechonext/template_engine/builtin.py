import os
import re
from loguru import logger
from pyechonext.request import Request
from pyechonext.utils.exceptions import TemplateNotFileError

FOR_BLOCK_PATTERN = re.compile(
	r"{% for (?P<variable>[a-zA-Z]+) in (?P<seq>[a-zA-Z]+) %}(?P<content>[\S\s]+)(?={% endfor %}){% endfor %}"
)
VARIABLE_PATTERN = re.compile(r"{{ (?P<variable>[a-zA-Z_]+) }}")


class TemplateEngine:
	"""
	This class describes a built-in template engine.
	"""

	def __init__(self, base_dir: str, templates_dir: str):
		"""
		Constructs a new instance.

		:param		base_dir:		The base dir
		:type		base_dir:		str
		:param		templates_dir:	The templates dir
		:type		templates_dir:	str
		"""
		self.templates_dir = os.path.join(base_dir, templates_dir)

	def _get_template_as_string(self, template_name: str) -> str:
		"""
		Gets the template as string.

		:param		template_name:		   The template name
		:type		template_name:		   str

		:returns:	The template as string.
		:rtype:		str

		:raises		TemplateNotFileError:  Template is not a file
		"""
		template_name = os.path.join(self.templates_dir, template_name)

		if not os.path.isfile(template_name):
			raise TemplateNotFileError(f'Template "{template_name}" is not a file')

		with open(template_name, "r") as file:
			content = file.read()

		return content

	def _build_block_of_template(self, context: dict, raw_template_block: str) -> str:
		"""
		Builds a block of template.

		:param		context:			 The context
		:type		context:			 dict
		:param		raw_template_block:	 The raw template block
		:type		raw_template_block:	 str

		:returns:	The block of template.
		:rtype:		str
		"""
		used_vars = VARIABLE_PATTERN.findall(raw_template_block)

		if used_vars is None:
			return raw_template_block

		for var in used_vars:
			var_in_template = "{{ %s }}" % (var)
			processed_template_block = re.sub(
				var_in_template, str(context.get(var, "")), raw_template_block
			)

		return processed_template_block

	def _build_statement_for_block(self, context: dict, raw_template_block: str) -> str:
		"""
		Build statement `for` block

		:param		context:			 The context
		:type		context:			 dict
		:param		raw_template_block:	 The raw template block
		:type		raw_template_block:	 str

		:returns:	The statement for block.
		:rtype:		str
		"""
		statement_for_block = FOR_BLOCK_PATTERN.search(raw_template_block)

		if statement_for_block is None:
			return raw_template_block

		builded_statement_block_for = ""

		for variable in context.get(statement_for_block.group("seq"), []):
			builded_statement_block_for += self._build_block_of_template(
				{**context, statement_for_block.group("variable"): variable},
				statement_for_block.group("content"),
			)

		processed_template_block = FOR_BLOCK_PATTERN.sub(
			builded_statement_block_for, raw_template_block
		)

		return processed_template_block

	def build(self, context: dict, template_name: str) -> str:
		"""
		Build template

		:param		context:		The context
		:type		context:		dict
		:param		template_name:	The template name
		:type		template_name:	str

		:returns:	raw template string
		:rtype:		str
		"""
		raw_template = self._get_template_as_string(template_name)

		processed_template = self._build_statement_for_block(context, raw_template)

		return self._build_block_of_template(context, processed_template)


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
	logger.warn(
		"Built-in template engine is under development and may be unstable or contain bugs"
	)

	assert request.settings.BASE_DIR
	assert request.settings.TEMPLATES_DIR

	engine = TemplateEngine(request.settings.BASE_DIR, request.settings.TEMPLATES_DIR)

	context = kwargs

	logger.debug(f"Built-in template engine: render {template_name} ({request.path})")

	return engine.build(context, template_name)
