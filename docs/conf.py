import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath(os.path.join("..", "..")))
sys.path.insert(0, os.path.abspath("../pyechonext"))
sys.path.insert(0, os.path.abspath("pyechonext"))

project = "pyEchoNext"
author = "Alexeev Bronislav"
version = "0.8.0"
release = "0.8"
project_copyright = "2025-2026, Alexeev Bronislav"

extensions = [
    "sphinx.ext.autodoc",  # autodoc from docstrings
    "sphinx.ext.viewcode",  # links to source code
    "sphinx.ext.napoleon",  # support google and numpy docs style
    "sphinx.ext.todo",  # support TODO
    "sphinx.ext.coverage",  # check docs coverage
    "sphinx.ext.ifconfig",  # directives in docs
    "sphinx.ext.autosummary",  # generating summary for code
    "sphinx.ext.intersphinx",
    "sphinx.ext.githubpages",
]

pygments_style = "gruvbox-dark"

autodoc_default_options: dict[str, bool | str] = {
    "members": True,
    "undoc-members": True,
    "private-members": True,
    "special-members": "__init__",
}

html_theme = "furo"  # theme
html_static_path = ["_static"]  # static dir
todo_include_todos = True  # include todo in docs
auto_doc_default_options = {"autosummary": True}

autodoc_mock_imports = []

extensions: list[str] = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.ifconfig",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
]

html_sidebars: dict[str, list[str]] = {
    "**": [
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        "versioning.html",
        "sidebar/scroll-end.html",
    ]
}


def skip(app, what, name, obj, would_skip, options):
    if name == "__init__":
        return False
    return would_skip


def setup(app):
    app.connect("autodoc-skip-member", skip)
