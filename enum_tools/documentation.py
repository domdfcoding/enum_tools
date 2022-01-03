#!/usr/bin/env python3
#
#  documentation.py
"""
Decorators to add docstrings to enum members from comments.
"""
#
#  Copyright (c) 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import ast
import inspect
import re
import sys
import tokenize
import warnings
from enum import Enum, EnumMeta
from textwrap import dedent
from typing import Iterable, List, Optional, Sequence, Tuple, TypeVar, Union

# 3rd party
import pygments.token  # type: ignore
from pygments.lexers.python import PythonLexer  # type: ignore

__all__ = [
		"get_tokens",
		"document_enum",
		"document_member",
		"parse_tokens",
		"get_base_indent",
		"DocumentedEnum",
		"get_dedented_line",
		"MultipleDocstringsWarning",
		]

_lexer = PythonLexer()

INTERACTIVE = bool(getattr(sys, "ps1", sys.flags.interactive))

EnumType = TypeVar("EnumType", bound=EnumMeta)


def get_tokens(line: str) -> List[Tuple]:
	"""
	Returns a list ot tokens generated from the given Python code.

	:param line: Line of Python code to tokenise.
	"""

	return list(_lexer.get_tokens(line))


def _docstring_from_expr(expr: ast.Expr) -> Optional[str]:
	"""
	Check if the expression is a docstring.

	:param expr:

	:returns: The cleaned docstring text if it is a docstring, or :py:obj:`None` if it isn't.
	"""

	# might be docstring
	docstring_node = expr.value
	if isinstance(docstring_node, ast.Str):
		text = docstring_node.s
	elif isinstance(docstring_node, ast.Constant) and isinstance(docstring_node.value, str):
		text = docstring_node.value
	else:
		# not a docstring
		return None

	return inspect.cleandoc(text)


def _docstring_from_eol_comment(
		source: str,
		node: Union[ast.Assign, ast.AnnAssign],
		) -> Optional[str]:
	"""
	Search for an end-of-line docstring comment (starts with ``# doc:``).

	:param source: The source of the Enum class.
	:param node: The AST node for the Enum member.
	"""

	toks = _tokenize_line(source.split('\n')[node.lineno - 1])
	comment_toks = [x for x in list(toks) if x.type == tokenize.COMMENT]
	if comment_toks:
		for match in re.finditer(r"(doc:\s*)([^#]*)(#|$)", comment_toks[0].string):
			if match.group(2):
				return match.group(2).rstrip()
	return None


def _docstring_from_sphinx_comment(
		source: str,
		node: Union[ast.Assign, ast.AnnAssign],
		) -> Optional[str]:
	"""
	Search for a Sphinx-style docstring comment (starts with ``#:``).

	:param source: The source of the Enum class.
	:param node: The AST node for the Enum member.
	"""

	for offset in range(node.lineno - 1, 0, -1):
		line = source.split('\n')[offset - 1]
		if line.strip():
			# contains non-whitespace

			try:
				toks = _tokenize_line(line)
			except (tokenize.TokenError, SyntaxError):
				return None

			# print(list(toks))
			comment_toks = [x for x in list(toks) if x.type == tokenize.COMMENT]
			if comment_toks:
				for match in re.finditer(r"(#:\s*)(.*)", comment_toks[0].string):
					if match.group(2):
						return match.group(2).rstrip()

			return None

	return None


def _tokenize_line(line: str) -> List[tokenize.TokenInfo]:
	"""
	Tokenize a single line of Python source code.

	:param line:
	"""

	def yielder():
		yield line

	return list(tokenize.generate_tokens(yielder().__next__))


class MultipleDocstringsWarning(UserWarning):
	"""
	Warning emitted when multiple docstrings are found for a single Enum member.

	.. versionadded:: 0.8.0

	:param member:
	:param docstrings: The list of docstrings found for the member.
	"""

	#: The member with multiple docstrings.
	member: Enum

	#: The list of docstrings found for the member.
	docstrings: Iterable[str]

	def __init__(self, member: Enum, docstrings: Iterable[str] = ()):
		self.member = member
		self.docstrings = docstrings

	def __str__(self) -> str:
		member_full_name = '.'.join([
				self.member.__class__.__module__,
				self.member.__class__.__name__,
				self.member.name,
				])
		return f"Found multiple docstrings for enum member <{member_full_name}>"


def document_enum(an_enum: EnumType) -> EnumType:
	"""
	Document all members of an enum by parsing a docstring from the Python source..

	The docstring can be added in several ways:

	#. A comment at the end the line, starting with ``doc:``:

	   .. code-block:: python

	       Running = 1  # doc: The system is running.

	#. A comment on the previous line, starting with ``#:``. This is the format used by Sphinx.

	   .. code-block:: python

	       #: The system is running.
	       Running = 1

	#. A string on the line *after* the attribute. This can be used for multiline docstrings.

	   .. code-block:: python

	       Running = 1
	       \"\"\"
	       The system is running.

	       Hello World
	       \"\"\"

	If more than one docstring format is found for an enum member
	a :exc:`MultipleDocstringsWarning` is emitted.

	:param an_enum: An :class:`~enum.Enum` subclass
	:type an_enum: :class:`enum.Enum`

	:returns: The same object passed as ``an_enum``. This allows this function to be used as a decorator.
	:rtype: :class:`enum.Enum`

	.. versionchanged:: 0.8.0  Added support for other docstring formats and multiline docstrings.
	"""

	if not isinstance(an_enum, EnumMeta):
		raise TypeError(f"'an_enum' must be an 'Enum', not {type(an_enum)}!")

	if not INTERACTIVE:
		return an_enum

	func_source = dedent(inspect.getsource(an_enum))
	func_source_tree = ast.parse(func_source)

	assert len(func_source_tree.body) == 1
	module_body = func_source_tree.body[0]
	assert isinstance(module_body, ast.ClassDef)
	class_body = module_body.body

	for idx, node in enumerate(class_body):
		targets = []

		if isinstance(node, ast.Assign):
			for t in node.targets:
				assert isinstance(t, ast.Name)
				targets.append(t.id)

		elif isinstance(node, ast.AnnAssign):
			assert isinstance(node.target, ast.Name)
			targets.append(node.target.id)
		else:
			continue

		assert isinstance(node, (ast.Assign, ast.AnnAssign))
		# print(targets)

		if idx + 1 == len(class_body):
			next_node = None
		else:
			next_node = class_body[idx + 1]

		docstring_candidates = []

		if isinstance(next_node, ast.Expr):
			# might be docstring
			docstring_candidates.append(_docstring_from_expr(next_node))

		# maybe no luck with """ docstring? look for EOL comment.
		docstring_candidates.append(_docstring_from_eol_comment(func_source, node))

		# check non-whitespace lines above for Sphinx-style comment.
		docstring_candidates.append(_docstring_from_sphinx_comment(func_source, node))

		docstring_candidates_nn = list(filter(None, docstring_candidates))
		if len(docstring_candidates_nn) > 1:
			# Multiple docstrings found, warn
			warnings.warn(MultipleDocstringsWarning(getattr(an_enum, targets[0]), docstring_candidates_nn))

		if docstring_candidates_nn:
			docstring = docstring_candidates_nn[0]

			for target in targets:
				getattr(an_enum, target).__doc__ = docstring

	return an_enum


def document_member(enum_member: Enum) -> None:
	"""
	Document a member of an enum by adding a comment to the end of the line that starts with ``doc:``.

	:param enum_member: A member of an :class:`~enum.Enum` subclass
	"""

	if not isinstance(enum_member, Enum):
		raise TypeError(f"'an_enum' must be an 'Enum', not {type(enum_member)}!")

	if not INTERACTIVE:
		return None

	func_source = dedent(inspect.getsource(enum_member.__class__))

	in_docstring = False
	base_indent = None

	for line in func_source.split('\n'):

		indent, line = get_dedented_line(line)

		if line.startswith("class") or not line:
			continue

		all_tokens = get_tokens(line)
		base_indent = get_base_indent(base_indent, all_tokens, indent)
		# print(all_tokens)

		if enum_member.name not in line:
			continue

		if all_tokens[0][0] in pygments.token.Literal.String:
			if all_tokens[0][1] in {'"""', "'''"}:  # TODO: handle the other quotes appearing in docstring
				in_docstring = not in_docstring

		if all_tokens[0][0] in pygments.token.Name and in_docstring:
			continue
		elif all_tokens[0][0] not in pygments.token.Name:
			continue
		else:
			if indent > base_indent:  # type: ignore
				continue
		enum_vars, doc = parse_tokens(all_tokens)

		for var in enum_vars:
			# print(repr(var))
			if not var.startswith('@'):
				if var == enum_member.name:
					enum_member.__doc__ = doc

	return None


def parse_tokens(all_tokens: Iterable["pygments.Token"]) -> Tuple[List, Optional[str]]:
	"""
	Parse the tokens representing a line of code to identify Enum members and ``doc:`` comments.

	:param all_tokens:

	:return: A list of the Enum members' names, and the docstring for them.
	"""

	enum_vars = []
	doc = None
	comment = ''

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

	return enum_vars, doc


def get_base_indent(
		base_indent: Optional[int],
		all_tokens: Sequence[Sequence],
		indent: int,
		) -> Optional[int]:
	"""
	Determine the base level of indentation (i.e. one level of indentation in from the ``c`` of ``class``).

	:param base_indent: The current base level of indentation
	:param all_tokens:
	:param indent: The current level of indentation

	:returns: The base level of indentation
	"""

	if not base_indent:
		if all_tokens[0][0] in pygments.token.Literal.String:
			if all_tokens[0][1] in {'"""', "'''"}:
				base_indent = indent
		elif all_tokens[0][0] in pygments.token.Keyword:
			base_indent = indent
		elif all_tokens[0][0] in pygments.token.Name:
			base_indent = indent

	return base_indent


class DocumentedEnum(Enum):
	"""
	An enum where docstrings are automatically added to members from comments starting with ``doc:``.

	.. note:: This class does not (yet) support the other docstring formats :deco:`~.document_enum` does.
	"""

	def __init__(self, value):
		document_member(self)
		# super().__init__(value)


def get_dedented_line(line: str) -> Tuple[int, str]:
	"""
	Returns the line without indentation, and the amount of indentation.

	:param line: A line of Python source code
	"""

	dedented_line = dedent(line)
	indent = len(line) - len(dedented_line)
	line = dedented_line.strip()

	return indent, line
