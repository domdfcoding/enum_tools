#!/usr/bin/env python3
#
#  autoenum.py
"""
A Sphinx directive for documenting :class:`Enums <enum.Enum>` in Python.
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
#  Parts based on https://github.com/sphinx-doc/sphinx
#  |  Copyright (c) 2007-2020 by the Sphinx team (see AUTHORS file).
#  |  BSD Licensed
#  |  All rights reserved.
#  |
#  |  Redistribution and use in source and binary forms, with or without
#  |  modification, are permitted provided that the following conditions are
#  |  met:
#  |
#  |  * Redistributions of source code must retain the above copyright
#  |   notice, this list of conditions and the following disclaimer.
#  |
#  |  * Redistributions in binary form must reproduce the above copyright
#  |   notice, this list of conditions and the following disclaimer in the
#  |   documentation and/or other materials provided with the distribution.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  |  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  |  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  |  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  |  HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  |  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  |  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  |  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  |  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  |  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  |  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
from contextlib import suppress
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, get_type_hints

# 3rd party
from docutils.nodes import Element  # nodep
from sphinx.application import Sphinx  # nodep
from sphinx.domains import ObjType  # nodep
from sphinx.domains.python import PyClasslike, PyXRefRole  # nodep
from sphinx.environment import BuildEnvironment  # nodep
from sphinx.ext.autodoc import (  # nodep
		ALL,
		INSTANCEATTR,
		SUPPRESS,
		AttributeDocumenter,
		ClassDocumenter,
		ClassLevelDocumenter,
		Documenter
		)
from sphinx.locale import _  # nodep
from sphinx.util.inspect import memory_address_re, safe_getattr  # nodep
from sphinx.util.typing import stringify as stringify_typehint  # nodep
from sphinx_toolbox.more_autodoc.typehints import format_annotation  # nodep
from sphinx_toolbox.utils import begin_generate  # nodep

# this package
from enum_tools import __version__, documentation
from enum_tools.utils import get_base_object, is_enum, is_flag

__all__ = ["EnumDocumenter", "EnumMemberDocumenter", "setup", "FlagDocumenter", "PyEnumXRefRole"]

documentation.INTERACTIVE = True


class EnumDocumenter(ClassDocumenter):
	r"""
	Sphinx autodoc :class:`~sphinx.ext.autodoc.Documenter` for documenting :class:`~enum.Enum`\s.
	"""

	objtype = "enum"
	directivetype = "enum"
	priority = 20
	class_xref = ":class:`~enum.Enum`"

	@classmethod
	def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
		"""
		Called to see if a member can be documented by this documenter.

		:param member:
		:param membername:
		:param isattr:
		:param parent:
		"""

		return is_enum(member) and not is_flag(member)

	def document_members(self, all_members: bool = False) -> None:
		"""
		Generate reST for member documentation.

		:param all_members: If :py:obj:`True`, document all members, otherwise document those given by
			else those given by ``self.options.members``.

		.. latex:clearpage::
		"""

		if self.doc_as_attr:
			return

		# print(self.directive.result)
		# input("> ")

		# set current namespace for finding members
		self.env.temp_data["autodoc:module"] = self.modname
		if self.objpath:
			self.env.temp_data["autodoc:class"] = self.objpath[0]

		want_all = all_members or self.options.inherited_members or self.options.members is ALL
		# find out which members are documentable
		members_check_module, members = self.get_object_members(want_all)

		non_enum_members = []
		for member in members:
			if member[0] not in self.object.__members__.keys():
				non_enum_members.append(member)

		user_option_undoc_members = self.options.undoc_members

		# Document enums first
		self.options.undoc_members = True  # type: ignore

		enum_members = [(var.name, var) for var in self.object]
		self._do_document_members(
				enum_members,
				want_all,
				members_check_module,
				description="Valid values are as follows:",
				)

		# Document everything else
		self.options.undoc_members = user_option_undoc_members  # type: ignore

		methods_text = (
				f"The {self.class_xref} and its members "
				f"{'also ' if enum_members else ''}have the following methods:"
				)

		self._do_document_members(
				non_enum_members,
				want_all,
				members_check_module,
				description=methods_text,
				)

	def _do_document_members(self, members, want_all, members_check_module, description):
		# remove members given by exclude-members
		if self.options.exclude_members:
			members = [
					(membername, member)
					for (membername, member) in members  # noqa
					if (self.options.exclude_members is ALL or membername not in self.options.exclude_members)
					]

		# document non-skipped members
		memberdocumenters: List[Tuple[Documenter, bool]] = []

		description_added = False

		for (mname, member, isattr) in self.filter_members(members, want_all):
			if not description_added:
				self.add_line(description, self.sourcename)
				self.add_line('', self.sourcename)
				description_added = True

			# give explicitly separated module name, so that members
			# of inner classes can be documented
			full_mname = self.modname + "::" + '.'.join(self.objpath + [mname])

			documenter: Documenter

			if isinstance(member, Enum) and member in self.object:
				documenter = EnumMemberDocumenter(self.directive, full_mname, self.indent)

			else:
				classes = [
						cls for cls in self.documenters.values()
						if cls.can_document_member(member, mname, isattr, self)
						]

				if not classes:
					# don't know how to document this member
					continue

				# prefer the documenter with the highest priority
				classes.sort(key=lambda cls: cls.priority)
				documenter = classes[-1](self.directive, full_mname, self.indent)

			memberdocumenters.append((documenter, isattr))

		member_order = self.options.member_order or self.env.config.autodoc_member_order

		if member_order == "groupwise":
			# sort by group; relies on stable sort to keep items in the
			# same group sorted alphabetically
			memberdocumenters.sort(key=lambda e: e[0].member_order)

		elif member_order == "bysource" and self.analyzer:
			# sort by source order, by virtue of the module analyzer
			tagorder = self.analyzer.tagorder

			def keyfunc(entry: Tuple[Documenter, bool]) -> int:
				fullname = entry[0].name.split("::")[1]
				return tagorder.get(fullname, len(tagorder))

			memberdocumenters.sort(key=keyfunc)

		for documenter, isattr in memberdocumenters:
			documenter.generate(
					all_members=True,
					real_modname=self.real_modname,
					check_module=members_check_module and not isattr,
					)

		# reset current objects
		self.env.temp_data["autodoc:module"] = None
		self.env.temp_data["autodoc:class"] = None

	real_modname: str

	def generate(
			self,
			more_content: Optional[Any] = None,
			real_modname: Optional[str] = None,
			check_module: bool = False,
			all_members: bool = False,
			) -> None:
		"""
		Generate reST for the object given by *self.name*, and possibly for its members.

		:param more_content: Additional content to include in the reST output.
		:param real_modname: Module name to use to find attribute documentation.
		:param check_module: If :py:obj:`True`, only generate if the object is defined
			in the module name it is imported from.
		:param all_members: If :py:obj:`True`, document all members.
		"""

		ret = begin_generate(self, real_modname, check_module)
		if ret is None:
			return
		sourcename = ret

		# Set sourcename as instance variable to avoid passing it around; it will get deleted later
		self.sourcename = sourcename

		# generate the directive header and options, if applicable
		self.add_directive_header("(value)")
		self.add_line('', sourcename)

		self.indent += self.content_indent

		# add all content (from docstrings, attribute docs etc.)
		self.add_content(more_content)

		member_type = get_base_object(self.object)

		if member_type is not object:
			# Show the type of the members
			self.add_line(f":Member Type: {format_annotation(member_type)}", self.sourcename)
			self.add_line('', self.sourcename)

		# document members, if possible
		self.document_members(all_members)
		del self.sourcename


class FlagDocumenter(EnumDocumenter):
	r"""
	Sphinx autodoc :class:`~sphinx.ext.autodoc.Documenter` for documenting :class:`~enum.Flag`\s.

	.. autosummary-widths:: 55/100
	"""

	objtype = "flag"
	directivetype = "flag"
	priority = 15
	class_xref = ":class:`~enum.Flag`"

	@classmethod
	def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
		"""
		Called to see if a member can be documented by this documenter.

		:param member:
		:param membername:
		:param isattr:
		:param parent:
		"""

		return is_flag(member)


class EnumMemberDocumenter(AttributeDocumenter):
	"""
	Sphinx autodoc :class:`~sphinx.ext.autodoc.Documenter` for documenting :class:`~enum.Enum` members.
	"""

	def import_object(self, raiseerror: bool = False) -> bool:
		"""
		Import the object given by ``self.modname`` and ``self.objpath`` and set it as ``self.object``.

		:param raiseerror:

		:returns: :py:obj:`True` if successful, :py:obj:`False` if an error occurred.

		.. latex:clearpage::
		"""

		return Documenter.import_object(self, raiseerror=raiseerror)

	def generate(
			self,
			more_content: Optional[Any] = None,
			real_modname: Optional[str] = None,
			check_module: bool = False,
			all_members: bool = False
			) -> None:
		"""
		Generate reST for the object given by ``self.name``, and possibly for its members.

		:param more_content: Additional content to include in the reST output.
		:param real_modname: Module name to use to find attribute documentation.
		:param check_module: If :py:obj:`True`, only generate if the object is defined in
			the module name it is imported from.
		:param all_members: If :py:obj:`True`, document all members.


		.. versionchanged:: 0.8.0

			Multiline docstrings are now correctly represented in the generated output.
		"""

		ret = begin_generate(self, real_modname, check_module)
		if ret is None:
			return

		sourcename = ret

		# generate the directive header and options, if applicable
		self.add_directive_header('')
		self.add_line('', sourcename)

		# e.g. the module directive doesn't have content
		self.indent += self.content_indent

		# Add the value's docstring
		if self.object.__doc__ and self.object.__doc__ != self.object.__class__.__doc__:
			# Lines of multiline docstrings need to be added one by one.
			for line in self.object.__doc__.splitlines():
				self.add_line(line, sourcename)
			self.add_line('', sourcename)

	def add_directive_header(self, sig: str) -> None:
		"""
		Add the directive header for the Enum member.

		:param sig:
		"""

		ClassLevelDocumenter.add_directive_header(self, sig)
		sourcename = self.get_sourcename()
		if not self.options.annotation:
			# obtain type annotation for this attribute
			try:
				annotations = get_type_hints(self.parent)
			except NameError:
				# Failed to evaluate ForwardRef (maybe TYPE_CHECKING)
				annotations = safe_getattr(self.parent, "__annotations__", {})
			except (TypeError, KeyError, AttributeError):
				# KeyError = a broken class found (refs: https://github.com/sphinx-doc/sphinx/issues/8084)
				# AttributeError is raised on 3.5.2 (fixed by 3.5.3)
				annotations = {}

			if self.objpath[-1] in annotations:
				objrepr = stringify_typehint(annotations.get(self.objpath[-1]))
				self.add_line("   :type: " + objrepr, sourcename)
			else:
				key = ('.'.join(self.objpath[:-1]), self.objpath[-1])
				if self.analyzer and key in self.analyzer.annotations:
					self.add_line("   :type: " + self.analyzer.annotations[key], sourcename)

		elif self.options.annotation is SUPPRESS:
			pass
		else:
			self.add_line("   :annotation: %s" % self.options.annotation, sourcename)

		if not self.options.annotation:
			with suppress(Exception):
				if self.object is not INSTANCEATTR:

					# Workaround for https://github.com/sphinx-doc/sphinx/issues/9272
					# which broke Enum displays in 4.1.0
					objrepr = memory_address_re.sub('', repr(self.object)).replace('\n', ' ')
					self.add_line(f'   :value: {objrepr}', self.get_sourcename())


class PyEnumXRefRole(PyXRefRole):
	"""
	XRefRole for Enum/Flag members.

	.. versionadded:: 0.4.0
	.. autosummary-widths:: 40/100
	"""

	def process_link(
			self,
			env: BuildEnvironment,
			refnode: Element,
			has_explicit_title: bool,
			title: str,
			target: str,
			) -> Tuple[str, str]:
		"""
		Called after parsing title and target text, and creating the reference node (given in ``refnode``).

		This method can alter the reference node and must return a new (or the same)
		``(title, target)`` tuple.

		:param env:
		:param refnode:
		:param has_explicit_title:
		:param title:
		:param target:

		:rtype:

		.. latex:clearpage::
		"""

		refnode["py:module"] = env.ref_context.get("py:module")
		refnode["py:class"] = env.ref_context.get("py:class")

		if not has_explicit_title:
			title = title.lstrip('.')  # only has a meaning for the target
			target = target.lstrip("~+")  # only has a meaning for the title
			# if the first character is a tilde, don't display the module/class
			# parts of the contents

			if title[0:1] == '~':
				title = '.'.join(title[1:].split('.')[-2:])

			elif title[0:1] == '+':
				title = title[1:]
				dot = title.rfind('.')
				if dot != -1:
					title = title[dot + 1:]

		# if the first character is a dot, search more specific namespaces first
		# else search builtins first
		if target[0:1] == '.':
			target = target[1:]
			refnode["refspecific"] = True

		return title, target


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup Sphinx Extension.

	:param app:
	"""

	app.registry.domains["py"].object_types["enum"] = ObjType(_("enum"), "enum", "class", "obj")
	app.add_directive_to_domain("py", "enum", PyClasslike)
	app.add_role_to_domain("py", "enum", PyXRefRole())

	app.registry.domains["py"].object_types["flag"] = ObjType(_("flag"), "flag", "enum", "class", "obj")
	app.add_directive_to_domain("py", "flag", PyClasslike)
	app.add_role_to_domain("py", "flag", PyXRefRole())

	app.add_role_to_domain("py", "enum:mem", PyEnumXRefRole())
	app.add_role_to_domain("py", "enum:member", PyEnumXRefRole())
	app.add_role_to_domain("py", "flag:mem", PyEnumXRefRole())
	app.add_role_to_domain("py", "flag:member", PyEnumXRefRole())

	app.add_autodocumenter(EnumDocumenter)
	app.add_autodocumenter(FlagDocumenter)

	return {
			"version": __version__,
			"parallel_read_safe": True,
			"parallel_write_safe": True,
			}
