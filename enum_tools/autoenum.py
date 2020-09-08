#!/usr/bin/env python3
#
#  autoenum.py
"""
A Sphinx directive for documenting Enums in Python.

Provides the ``.. autoenum::`` directive to document an enum.
It behaves much like ``.. autoclass::`` and ``.. autofunction::``.
"""
# See also https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import inspect
from enum import Enum, EnumMeta, Flag
from typing import Any, Dict, List, Optional, Tuple, Type

# 3rd party
from sphinx.application import Sphinx
from sphinx.domains import ObjType
from sphinx.domains.python import PyClasslike, PyXRefRole
from sphinx.errors import PycodeError
from sphinx.ext.autodoc import ALL, AttributeDocumenter, ClassDocumenter, Documenter, logger
from sphinx.locale import _, __
from sphinx.pycode import ModuleAnalyzer
from enum_tools._autodoc_typehints import format_annotation

# this package
from enum_tools import __version__, documentation

__all__ = ["EnumDocumenter", "EnumMemberDocumenter", "setup"]

documentation.INTERACTIVE = True


def get_base_object(enum: EnumMeta) -> Type:
	"""
	Returns the object type of the enum's members

	If the members are of indeterminate type :class`object` is returned.
	"""

	mro = inspect.getmro(enum)
	if Flag in mro:
		mro = mro[:mro.index(Flag)]
	elif Enum in mro:
		mro = mro[:mro.index(Enum)]
	else:
		raise TypeError("not an Enum")

	mro = mro[1:]

	for obj in mro:
		if not isinstance(obj, EnumMeta):
			return obj

	return object


def _start_generate(
		documenter,
		real_modname: Optional[str] = None,
		check_module: bool = False,
		) -> Optional[str]:
	"""
	Boilerplate for the top of ``generate`` in :class:`EnumDocumenter` and :class:`EnumMemberDocumenter`.

	:param documenter:
	:param real_modname:
	:param check_module:

	:return: The ``sourcename``, or None if certain conditions are met,
		to indicate that the Documenter class should exit early.
	"""

	# Do not pass real_modname and use the name from the __module__
	# attribute of the class.
	# If a class gets imported into the module real_modname
	# the analyzer won't find the source of the class, if
	# it looks in real_modname.

	if not documenter.parse_name():
		# need a module to import
		logger.warning(
				__(
						"don't know which module to import for autodocumenting "
						f'{documenter.name!r} (try placing a "module" or "currentmodule" directive '
						"in the document, or giving an explicit module name)"
						),
				type="autodoc"
				)
		return None

	# now, import the module and get object to document
	if not documenter.import_object():
		return None

	# If there is no real module defined, figure out which to use.
	# The real module is used in the module analyzer to look up the module
	# where the attribute documentation would actually be found in.
	# This is used for situations where you have a module that collects the
	# functions and classes of internal submodules.
	documenter.real_modname = real_modname or documenter.get_real_modname()

	# try to also get a source code analyzer for attribute docs
	try:
		documenter.analyzer = ModuleAnalyzer.for_module(documenter.real_modname)
		# parse right now, to get PycodeErrors on parsing (results will
		# be cached anyway)
		documenter.analyzer.find_attr_docs()

	except PycodeError as err:
		logger.debug("[autodoc] module analyzer failed: %s", err)
		# no source file -- e.g. for builtin and C modules
		documenter.analyzer = None
		# at least add the module.__file__ as a dependency
		if hasattr(documenter.module, "__file__") and documenter.module.__file__:
			documenter.directive.filename_set.add(documenter.module.__file__)
	else:
		documenter.directive.filename_set.add(documenter.analyzer.srcname)

	# check __module__ of object (for members not given explicitly)
	if check_module:
		if not documenter.check_module():
			return None

	sourcename = documenter.get_sourcename()

	# make sure that the result starts with an empty line.  This is
	# necessary for some situations where another directive preprocesses
	# reST and no starting newline is present
	documenter.add_line('', sourcename)

	return sourcename


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

		# The enum itself is subclass of EnumMeta; enum members subclass Enum
		return isinstance(member, EnumMeta)

	def document_members(self, all_members: bool = False) -> None:
		"""
		Generate reST for member documentation.

		:param all_members: If :py:obj:`True`, document all members, otherwise document those given by
			else those given by ``self.options.members``.
		"""

		if self.doc_as_attr:
			return

		print(self.directive.result)
		input("> ")

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

		ret = _start_generate(self, real_modname, check_module)
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
	"""

	objtype = "flag"
	directivetype = "flag"
	priority = 19
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

		# The enum itself is subclass of EnumMeta; enum members subclass Enum
		if isinstance(member, EnumMeta):
			for attr in {"__or__", "__and__", "__xor__", "__invert__"}:
				if not hasattr(member, attr):
					return False

			return True
		else:
			return False


class EnumMemberDocumenter(AttributeDocumenter):
	"""
	Sphinx autodoc :class:`~sphinx.ext.autodoc.Documenter` for documenting :class:`~enum.Enum` members.
	"""

	def import_object(self, raiseerror: bool = False) -> Any:
		"""
		Import the object given by ``self.modname`` and ``self.objpath`` and set it as ``self.object``.

		:param raiseerror:

		:returns: :py:obj:`True` if successful, :py:obj:`False` if an error occurred.
		"""

		self._datadescriptor = False
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
		"""

		ret = _start_generate(self, real_modname, check_module)
		if ret is None:
			return

		sourcename = ret

		# generate the directive header and options, if applicable
		self.add_directive_header('')
		self.add_line('', sourcename)

		# e.g. the module directive doesn't have content
		self.indent += self.content_indent

		# Add the value's docstring
		if self.object.__doc__ and self.object.__doc__ != self.object.__class__:
			self.add_line(self.object.__doc__, sourcename)
			self.add_line('', sourcename)


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

	app.add_autodocumenter(EnumDocumenter)
	app.add_autodocumenter(FlagDocumenter)

	return {
			"version": __version__,
			"parallel_read_safe": True,
			"parallel_write_safe": True,
			}
