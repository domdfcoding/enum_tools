#!/usr/bin/env python3
#
#  custom_enums.py
"""
Custom subclasses of :class:`enum.Enum` and :class:`enum.Flag`.
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
import sys
from enum import Enum, Flag, IntFlag
from typing import Any, Iterator

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

if sys.version_info >= (3, 11):  # pragma: no cover

	# stdlib
	from enum import _power_of_two

	def _decompose(flag, value):
		"""
		Extract all members from the value.
		"""

		# From CPython. Removed in https://github.com/python/cpython/pull/24215

		# _decompose is only called if the value is not named
		not_covered = value

		# issue29167: wrap accesses to _value2member_map_ in a list to avoid race
		#             conditions between iterating over it and having more pseudo-
		#             members added to it

		flags_to_check = []

		if value < 0:
			# only check for named flags
			for v, m in list(flag._value2member_map_.items()):
				if m.name is not None:
					flags_to_check.append((m, v))
		else:
			# check for named flags and powers-of-two flags
			for v, m in list(flag._value2member_map_.items()):
				if m.name is not None or _power_of_two(v):
					flags_to_check.append((m, v))

		members = []

		for member, member_value in flags_to_check:
			if member_value and member_value & value == member_value:
				members.append(member)
				not_covered &= ~member_value

		if not members and value in flag._value2member_map_:
			members.append(flag._value2member_map_[value])

		members.sort(key=lambda m: m._value_, reverse=True)

		if len(members) > 1 and members[0].value == value:
			# we have the breakdown, don't need the value member itself
			members.pop(0)

		return members, not_covered

else:  # pragma: no cover (py310+)

	# stdlib
	from enum import _decompose  # type: ignore


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
		member = str.__new__(cls, value)
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
	:class:`~enum.Flag` with support for iterating over members and member combinations.

	This functionality was added to Python 3.10's :mod:`enum` module in :pull:`22221 <python/cpython>`.

	.. versionadded:: 0.5.0
	"""

	def __iter__(self) -> Iterator[Flag]:
		"""
		Returns members in definition order.

		:rtype:

		.. latex:clearpage::
		"""

		members, extra_flags = _decompose(self.__class__, self.value)
		return (m for m in members if m._value_ != 0)


class IterableIntFlag(IntFlag):
	"""
	:class:`~enum.IntFlag` with support for iterating over members and member combinations.

	This functionality was added to Python 3.10's :mod:`enum` module in :pull:`22221 <python/cpython>`.

	.. versionadded:: 0.5.0
	"""

	def __iter__(self) -> Iterator[IntFlag]:
		"""
		Returns members in definition order.
		"""

		members, extra_flags = _decompose(self.__class__, self.value)
		return (m for m in members if m._value_ != 0)
