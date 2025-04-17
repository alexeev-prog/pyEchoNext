# project = "pyechonext"
# author = "Alexeev Bronislav"
# version = "0.1"
# release = "0.1.0"

# extensions = [
# 	"sphinx.ext.autodoc",
# 	"sphinx.ext.viewcode",
# 	"sphinx.ext.napoleon",
# 	"sphinx.ext.coverage",
# 	"sphinx.ext.ifconfig",
# 	"sphinx.ext.graphviz",
# ]

# html_theme = "sphinx_rtd_theme"
# html_static_path = ["_static"]
# todo_include_todos = True

# autodock_mock_imports = []

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'pyEchoNext'
author = 'name'
version = '0.7.14'
release = '0.7'

extensions = [
    'sphinx.ext.autodoc',  # авто документации из docstrings
    'sphinx.ext.viewcode',  # ссылки на исходный код
    'sphinx.ext.napoleon',  # поддержка Google и NumPy стиля документации
    'sphinx.ext.todo',  # поддержка TODO
    'sphinx.ext.coverage',  # проверяет покрытие документации
    'sphinx.ext.ifconfig',  # условные директивы в документации
]

html_theme = 'furo'  # тема оформления
html_static_path = ['_static']  # папка со статическими файлами (например, CSS)
todo_include_todos = True  # показывать TODO в готовой документации

# autodoc_mock_imports = ["тяжеловесные_модули"]  # модули для мокирования
