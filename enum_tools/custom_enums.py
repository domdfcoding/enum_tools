#!/usr/bin/env python3
#
#  custom_enums.py
"""
Custom subclasses of :class:`enum.Enum` and :class:`enum.Flag`.
"""
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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Parts based on https://docs.python.org/3/library/enum.html
#  and https://github.com/python/cpython/pull/22221
#  and https://github.com/python/cpython/pull/22337
#  PSF License 2.0
#

# stdlib
from enum import Enum, Flag, IntFlag, _decompose  # type: ignore
from typing import Any

__all__ = [
		"MemberDirEnum",
		"IntEnum",
		"StrEnum",
		"AutoNumberEnum",
		"OrderedEnum",
		"DuplicateFreeEnum",
		"IterableFlag",
		"IterableIntFlag",
		]


class MemberDirEnum(Enum):
	"""
	:class:`~enum.Enum` which includes attributes as well as methods.

	This will be part of the :mod:`enum` module starting with Python 3.10.

	.. seealso:: Pull request :pull:`19219 <python/cpython>` by Angelin BOOZ, which added this to CPython.

	.. versionadded:: 0.6.0
	"""

	def __dir__(self):
		return super().__dir__() + [m for m in self.__dict__ if m[0] != '_']


class IntEnum(int, Enum):
	"""
	:class:`~enum.Enum` where members are also (and must be) ints.
	"""


# 	def __int__(self):
# 		return self.value

# 	def __eq__(self, other):
# 		if int(self) == other:
# 			return True
# 		else:
# 			return super().__eq__(other)


class StrEnum(str, Enum):
	"""
	:class:`~enum.Enum` where members are also (and must be) strings.
	"""

	def __str__(self) -> str:
		return self.value

	def __new__(cls, *values):  # noqa: D102
		if len(values) > 3:
			raise TypeError(f'too many arguments for str(): {values!r}')
		if len(values) == 1:
			# it must be a string
			if not isinstance(values[0], str):
				raise TypeError(f'{values[0]!r} is not a string')
		if len(values) > 1:
			# check that encoding argument is a string
			if not isinstance(values[1], str):
				raise TypeError(f'encoding must be a string, not {values[1]!r}')
			if len(values) > 2:
				# check that errors argument is a string
				if not isinstance(values[2], str):
					raise TypeError(f'errors must be a string, not {values[2]!r}')
		value = str(*values)
		member = str.__new__(cls, value)  # type: ignore
		member._value_ = value
		return member

	# def __repr__(self):
	# 	return self.value

	# def __eq__(self, other):
	# 	if str(self) == other:
	# 		return True
	# 	else:
	# 		return super().__eq__(other)


class AutoNumberEnum(Enum):
	"""
	:class:`~enum.Enum` that automatically assigns increasing values to members.
	"""

	def __new__(cls, *args, **kwds) -> Any:  # noqa: D102
		value = len(cls.__members__) + 1
		obj = object.__new__(cls)
		obj._value_ = value
		return obj


class OrderedEnum(Enum):
	"""
	:class:`~enum.Enum` that adds ordering based on the values of its members.
	"""

	def __ge__(self, other) -> bool:
		if self.__class__ is other.__class__:
			return self._value_ >= other._value_
		return NotImplemented

	def __gt__(self, other) -> bool:
		if self.__class__ is other.__class__:
			return self._value_ > other._value_
		return NotImplemented

	def __le__(self, other) -> bool:
		if self.__class__ is other.__class__:
			return self._value_ <= other._value_
		return NotImplemented

	def __lt__(self, other) -> bool:
		if self.__class__ is other.__class__:
			return self._value_ < other._value_
		return NotImplemented


class DuplicateFreeEnum(Enum):
	"""
	:class:`~enum.Enum` that disallows duplicated member names.
	"""

	def __init__(self, *args) -> None:
		cls = self.__class__
		if any(self.value == e.value for e in cls):
			a = self.name
			e = cls(self.value).name
			raise ValueError(f"aliases are not allowed in DuplicateFreeEnum:  {a!r} --> {e!r}")


class IterableFlag(Flag):
	"""
	:class:`enum.Flag` with support for iterating over members and member combinations.

	This functionality was added to Python 3.10's :mod:`enum` module in :pull:`22221 <python/cpython>`.

	.. versionadded:: 0.5.0
	"""

	def __iter__(self):
		members, extra_flags = _decompose(self.__class__, self.value)
		return (m for m in members if m._value_ != 0)


class IterableIntFlag(IntFlag):
	"""
	:class:`enum.IntFlag` with support for iterating over members and member combinations.

	This functionality was added to Python 3.10's :mod:`enum` module in :pull:`22221 <python/cpython>`.

	.. versionadded:: 0.5.0
	"""

	def __iter__(self):
		members, extra_flags = _decompose(self.__class__, self.value)
		return (m for m in members if m._value_ != 0)
