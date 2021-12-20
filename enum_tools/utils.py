#!/usr/bin/env python3
#
#  utils.py
"""
General utility functions.
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
from enum import Enum, EnumMeta, Flag
from typing import Tuple, Type

# 3rd party
from typing_extensions import Protocol, runtime_checkable

__all__ = ["HasMRO", "is_enum", "is_enum_member", "is_flag", "get_base_object"]


@runtime_checkable
class HasMRO(Protocol):
	"""
	:class:`typing.Protocol` for classes that have a method resolution order magic method (``__mro__``).
	"""

	@property
	def __mro__(self) -> Tuple[Type]: ...


def is_enum(obj: Type) -> bool:
	"""
	Returns :py:obj:`True` if ``obj`` is an :class:`enum.Enum`.

	:param obj:
	"""

	# The enum itself is subclass of EnumMeta; enum members subclass Enum
	return isinstance(obj, EnumMeta)


def is_enum_member(obj: Type) -> bool:
	"""
	Returns :py:obj:`True` if ``obj`` is an :class:`enum.Enum` member.

	:param obj:
	"""

	# The enum itself is subclass of EnumMeta; enum members subclass Enum
	return isinstance(obj, Enum)


def is_flag(obj: Type) -> bool:
	"""
	Returns :py:obj:`True` if ``obj`` is an :class:`enum.Flag`.

	:param obj:
	"""

	# The enum itself is subclass of EnumMeta; enum members subclass Enum
	if is_enum(obj) and isinstance(obj, HasMRO):
		return Flag in inspect.getmro(obj)
	else:
		return False


def get_base_object(enum: Type[HasMRO]) -> Type:
	"""
	Returns the object type of the enum's members.

	If the members are of indeterminate type then the :class:`object` class is returned.

	:param enum:

	:rtype:

	:raises TypeError: If ``enum`` is not an Enum.
	"""

	try:
		mro = inspect.getmro(enum)
	except AttributeError:
		raise TypeError("not an Enum")

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
