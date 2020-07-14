#!/usr/bin/env python3
#
#  _custom_enums.py
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
#

# stdlib
from enum import Enum

__all__ = [
		"IntEnum",
		"StrEnum",
		"AutoNumberEnum",
		"OrderedEnum",
		"DuplicateFreeEnum",
		]


class IntEnum(int, Enum):  # pylint: disable=used-before-assignment
	"""
	Enum where members are also (and must be) ints
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
	Enum where members are also (and must be) strings
	"""

	def __str__(self) -> str:
		return self.value

	# def __repr__(self):
	# 	return self.value

	# def __eq__(self, other):
	# 	if str(self) == other:
	# 		return True
	# 	else:
	# 		return super().__eq__(other)


class AutoNumberEnum(Enum):
	"""
	Automatically assign increasing values to members.
	"""

	def __new__(cls, *args, **kwds):
		value = len(cls.__members__) + 1
		obj = object.__new__(cls)
		obj._value_ = value
		return obj


class OrderedEnum(Enum):
	"""
	Add ordering based on values of Enum members.
	"""

	def __ge__(self, other):
		if self.__class__ is other.__class__:
			return self._value_ >= other._value_
		return NotImplemented

	def __gt__(self, other):
		if self.__class__ is other.__class__:
			return self._value_ > other._value_
		return NotImplemented

	def __le__(self, other):
		if self.__class__ is other.__class__:
			return self._value_ <= other._value_
		return NotImplemented

	def __lt__(self, other):
		if self.__class__ is other.__class__:
			return self._value_ < other._value_
		return NotImplemented


class DuplicateFreeEnum(Enum):
	"""
	Enum subclass that disallows duplicated member names
	"""

	def __init__(self, *args):
		cls = self.__class__
		if any(self.value == e.value for e in cls):
			a = self.name
			e = cls(self.value).name
			raise ValueError(f"aliases not allowed in DuplicateFreeEnum:  {a!r} --> {e!r}")
