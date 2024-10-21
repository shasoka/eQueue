# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys


if sys.platform == "win32":
    sys.path.insert(0, os.path.abspath("../eQueue"))

project = "eQueue API"
copyright = "Copyright (c) YYYY Arkady Schoenberg <shasoka@yandex.ru>"
author = "Arkady Schoenberg"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autodoc_mock_imports = [
    "core.config",
    "moodle.courses",
    "api",
    "api.api_v1.groups",
    "api.api_v1.queue_websocket",
    "api.api_v1.subjects",
    "api.api_v1.users",
    "api.api_v1.workspaces",
    "api.api_v1",
    "core.models.base",
    "core.models.db",
    "core.models.entities",
    "core.models",
    "crud.assignments",
    "crud.groups",
    "crud.queues",
    "crud.subjects",
    "crud.users",
    "crud.workspaces",
    "main",
    "moodle.auth.oauth2",
    "moodle.auth",
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
