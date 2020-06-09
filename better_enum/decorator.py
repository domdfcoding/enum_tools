# stdlib
import inspect
import re
from textwrap import dedent
from typing import TYPE_CHECKING

# 3rd party
import pygments.token  # type: ignore
from pygments.lexers import PythonLexer  # type: ignore
from .importer import EnumMeta


def document(an_enum):
	if not isinstance(an_enum, EnumMeta):
		raise TypeError(f"'an_enum' must be an `aenum.Enum`, not {type(an_enum)}!")

	func_source = inspect.getsource(an_enum)

	in_docstring = False
	base_indent = None

	func_source = dedent(func_source)

	for line in func_source.split("\n"):

		dedented_line = dedent(line)
		indent = len(line) - len(dedented_line)
		line = dedented_line.strip()

		if line.startswith("class") or not line:
			continue

		enum_vars = []
		comment = ''
		doc = None

		all_tokens = list(PythonLexer().get_tokens(line))
		# print(all_tokens)

		if not base_indent:
			if all_tokens[0][0] in pygments.token.Literal.String:
				if all_tokens[0][1] in {'"""', "'''"}:
					base_indent = indent
			elif all_tokens[0][0] in pygments.token.Keyword:
				base_indent = indent
			elif all_tokens[0][0] in pygments.token.Name:
				base_indent = indent
		#

		if all_tokens[0][0] in pygments.token.Literal.String:
			if all_tokens[0][1] in {'"""', "'''"}:  # TODO: handle the other quotes appearing in docstring
				in_docstring = not in_docstring

		#

		if all_tokens[0][0] in pygments.token.Name and in_docstring:
			continue
		elif all_tokens[0][0] not in pygments.token.Name:
			continue
		else:
			if indent > base_indent:
				continue
		#

		for token in all_tokens:
			if token[0] in pygments.token.Name:
				enum_vars.append(token[1])
			elif token[0] in pygments.token.Comment:
				comment = token[1]
				break

		for match in re.finditer(r"(doc:\s*)([^#]*)(#|$)", comment):
			if match.group(2):
				doc = match.group(2).rstrip()
				break

		# print(line)
		# print(enum_vars)
		# print(doc)

		for var in enum_vars:
			print(repr(var))
			if not var.startswith("@"):
				getattr(an_enum, var).__doc__ = doc

	return an_enum
