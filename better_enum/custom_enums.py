#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
#  Based on aenum
#  https://bitbucket.org/stoneleaf/aenum
#  Copyright (c) 2015, 2016, 2017, 2018 Ethan Furman.
#  All rights reserved.
#  Licensed under the 3-clause BSD License:
#  |  Redistribution and use in source and binary forms, with or without
#  |  modification, are permitted provided that the following conditions
#  |  are met:
#  |
#  |      Redistributions of source code must retain the above
#  |      copyright notice, this list of conditions and the
#  |      following disclaimer.
#  |
#  |      Redistributions in binary form must reproduce the above
#  |      copyright notice, this list of conditions and the following
#  |      disclaimer in the documentation and/or other materials
#  |      provided with the distribution.
#  |
#  |      Neither the name Ethan Furman nor the names of any
#  |      contributors may be used to endorse or promote products
#  |      derived from this software without specific prior written
#  |      permission.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  |  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  |  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  |  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  |  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  |  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  |  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  |  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  |  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  |  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  |  POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
import sqlite3
import sys
from typing import TYPE_CHECKING

# this package
from ._constant import AutoValue, MultiValue, NoAlias, Unique
from .utils import _reduce_ex_by_name

if TYPE_CHECKING:
	from enum import Enum

else:
	from aenum import AutoValue, Enum, MultiValue, NoAlias, Unique

__all__ = [
		"IntEnum",
		"StrEnum",
		"AutoEnum",
		"AutoNumberEnum",
		"MultiValueEnum",
		"NoAliasEnum",
		"OrderedEnum",
		"SqliteEnum",
		"UniqueEnum",
		"convert",
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


class AutoEnum(Enum):
	"""
	automatically use _generate_next_value_ when values are missing (Python 3 only)
	"""
	_settings_ = AutoValue


class AutoNumberEnum(Enum):
	"""
	Automatically assign increasing values to members.

	Py3: numbers match creation order
	Py2: numbers are assigned alphabetically by member name
	"""

	def __new__(cls, *args, **kwds):
		value = len(cls.__members__) + 1
		obj = object.__new__(cls)
		obj._value_ = value
		return obj


class MultiValueEnum(Enum):
	"""
	Multiple values can map to each member.
	"""
	_settings_ = MultiValue


class NoAliasEnum(Enum):
	"""
	Duplicate value members are distinct, and cannot be looked up by value.
	"""
	_settings_ = NoAlias


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


class SqliteEnum(Enum):

	def __conform__(self, protocol):
		if protocol is sqlite3.PrepareProtocol:
			return self.name


class UniqueEnum(Enum):
	"""
	Ensure no duplicate values exist.
	"""
	_settings_ = Unique


def convert(enum, name, module, filter, source=None):
	"""
	Create a new Enum subclass that replaces a collection of global constants

	enum: Enum, IntEnum, ...
	name: name of new Enum
	module: name of module (__name__ in global context)
	filter: function that returns True if name should be converted to Enum member
	source: namespace to check (defaults to 'module')
	"""
	# convert all constants from source (or module) that pass filter() to
	# a new Enum called name, and export the enum and its members back to
	# module;
	# also, replace the __reduce_ex__ method so unpickling works in
	# previous Python versions
	module_globals = vars(sys.modules[module])
	if source:
		source = vars(source)
	else:
		source = module_globals
	members = dict((name, value) for name, value in source.items() if filter(name))
	enum = enum(name, members, module=module)
	enum.__reduce_ex__ = _reduce_ex_by_name
	module_globals.update(enum.__members__)
	module_globals[name] = enum
