#!/usr/bin/env python3

# This file is managed by 'repo_helper'. Don't edit it directly.

# stdlib
import os
import re
import sys

# 3rd party
from sphinx_pyproject import SphinxConfig

sys.path.append('.')

config = SphinxConfig(globalns=globals())
project = config["project"]
author = config["author"]
documentation_summary = config.description

github_url = "https://github.com/{github_username}/{github_repository}".format_map(config)

rst_prolog = f""".. |pkgname| replace:: enum_tools
.. |pkgname2| replace:: ``enum_tools``
.. |browse_github| replace:: `Browse the GitHub Repository <{github_url}>`__
"""

slug = re.sub(r'\W+', '-', project.lower())
release = version = config.version

todo_include_todos = bool(os.environ.get("SHOW_TODOS", 0))

intersphinx_mapping = {
		"python": ("https://docs.python.org/3/", None),
		"sphinx": ("https://www.sphinx-doc.org/en/stable/", None),
		}

html_theme_options = {"logo_only": False}

html_context = {
		"display_github": True,
		"github_user": "domdfcoding",
		"github_repo": "enum_tools",
		"github_version": "master",
		"conf_py_path": "/doc-source/",
		}
htmlhelp_basename = slug

latex_documents = [("index", f'{slug}.tex', project, author, "manual")]
man_pages = [("index", slug, project, [author], 1)]
texinfo_documents = [("index", slug, project, author, slug, project, "Miscellaneous")]

toctree_plus_types = set(config["toctree_plus_types"])

autodoc_default_options = {
		"members": None,  # Include all members (methods).
		"special-members": None,
		"autosummary": None,
		"show-inheritance": None,
		"exclude-members": ','.join(config["autodoc_exclude_members"]),
		}

latex_elements = {
		"printindex": "\\begin{flushleft}\n\\printindex\n\\end{flushleft}",
		"tableofcontents": "\\pdfbookmark[0]{\\contentsname}{toc}\\sphinxtableofcontents",
		}


def setup(app):
	# 3rd party
	from sphinx_toolbox.latex import better_header_layout

	app.connect("config-inited", lambda app, config: better_header_layout(config))


html_logo = "../enum_tools.png"
autosummary_widths_builders = ["latex"]
nitpicky = True
needspace_amount = "1\\baselineskip"
ignore_missing_xrefs = [
		"^sphinx.ext.autodoc.(Class|Attribute)?Documenter$",
		"^enum.EnumMeta$",
		"^docutils.nodes.Element$",
		"^sphinx.domains"
		]
# stdlib
from typing import Type

# 3rd party
import enum_tools.autoenum
from sphinx.ext.autodoc.directive import DocumenterBridge

enum_tools.autoenum.DocumenterBridge = DocumenterBridge
enum_tools.autoenum.Type = Type
