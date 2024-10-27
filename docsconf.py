project = "pyechonext"
author = "Alexeev Bronislav"
version = "0.1"
release = "0.1.0"

extensions = [
	"sphinx.ext.autodoc",
	"sphinx.ext.viewcode",
	"sphinx.ext.napoleon",
	"sphinx.ext.coverage",
	"sphinx.ext.ifconfig",
	"sphinx.ext.graphviz",
]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
todo_include_todos = True

autodock_mock_imports = []
