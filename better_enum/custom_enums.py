# stdlib
import sqlite3
import sys
from typing import TYPE_CHECKING

# this package
from .constant import AutoValue, MultiValue, NoAlias, Unique
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


class IntEnum(int, Enum):
	"""
	Enum where members are also (and must be) ints
	"""


#
# 	def __int__(self):
# 		return self.value
#
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

	#
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
