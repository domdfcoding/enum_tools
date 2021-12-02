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
import inspect
import re
import sys
from enum import Enum, EnumMeta
from textwrap import dedent
from typing import Iterable, List, Optional, Sequence, Tuple, TypeVar

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


def document_enum(an_enum: EnumType) -> EnumType:
	"""
	Document all members of an enum by adding a comment to the end of each line that starts with ``doc:``.

	:param an_enum: An :class:`~enum.Enum` subclass
	"""

	if not isinstance(an_enum, EnumMeta):
		raise TypeError(f"'an_enum' must be an 'Enum', not {type(an_enum)}!")

	if not INTERACTIVE:
		return an_enum

	func_source = dedent(inspect.getsource(an_enum))

	in_docstring = False
	base_indent = None

	source_lines = func_source.split('\n')

	while source_lines[0].startswith('@'):
		# Remove class decorators
		source_lines.pop(0)

	for line in source_lines:

		indent, line = get_dedented_line(line)

		if line.startswith("class") or not line:
			continue

		all_tokens = get_tokens(line)
		base_indent = get_base_indent(base_indent, all_tokens, indent)
		# print(all_tokens)

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

		# print(line)
		# print(enum_vars)
		# print(doc)

		for var in enum_vars:
			# print(repr(var))
			if not var.startswith('@'):
				getattr(an_enum, var).__doc__ = doc

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
