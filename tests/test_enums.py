"""
test_enums
~~~~~~~~~~~~~~~
"""

# stdlib
import sys
from enum import Enum

# 3rd party
import pytest

# this package
from enum_tools import IntEnum, StrEnum
from enum_tools.custom_enums import AutoNumberEnum, IterableFlag, IterableIntFlag, MemberDirEnum, OrderedEnum

NEW_ENUM_REPR = sys.version_info >= (3, 14)

xfail_314 = pytest.mark.xfail(
		reason="Python 3.14 behaviour has not been finalised yet.",
		condition=sys.version_info[:2] == (3, 14) and sys.version_info.releaselevel == "alpha"
		)


class DramatisPersonae(StrEnum):
	Message = "a secret message"
	Bob = "The sender"
	Alice = "The recipient"
	Chuck = "A man of malicious intent"
	Craig = "A password cracker"
	Eve = "An eavesdropper"


@xfail_314
def test_str_enum():
	assert DramatisPersonae.Message == "a secret message"
	assert DramatisPersonae.Alice != "An eavesdropper"
	assert str(DramatisPersonae.Craig) == "A password cracker"
	assert DramatisPersonae("The sender") == DramatisPersonae.Bob == "The sender"

	if NEW_ENUM_REPR:
		assert repr(DramatisPersonae.Bob) == "DramatisPersonae.Bob"
	else:
		assert repr(DramatisPersonae.Bob) == "<DramatisPersonae.Bob: 'The sender'>"


class Numbers(IntEnum):
	One = 1
	Two = 2
	Three = 3
	Four = 4
	Five = 5


def test_int_enum():
	assert Numbers.One == 1
	assert Numbers.Two != 3
	assert int(Numbers.Four) == 4
	assert Numbers(5) == Numbers.Five == 5
	assert isinstance(Numbers(5), int)


# The following from https://github.com/python/cpython/pull/22221/files
# PSF Licsense 2.0


def test_member_iter_int_flag():

	class Color(IterableIntFlag):
		BLACK = 0
		RED = 1
		GREEN = 2
		BLUE = 4
		PURPLE = RED | BLUE

	assert list(Color.PURPLE) == [Color.BLUE, Color.RED]
	assert list(Color.BLUE) == [Color.BLUE]
	assert list(Color.GREEN) == [Color.GREEN]


def test_member_iter_flag():

	class Color(IterableFlag):
		BLACK = 0
		RED = 1
		GREEN = 2
		BLUE = 4
		PURPLE = RED | BLUE

	assert list(Color.PURPLE) == [Color.BLUE, Color.RED]
	assert list(Color.BLUE) == [Color.BLUE]
	assert list(Color.GREEN) == [Color.GREEN]


def test_strenum():
	# From https://github.com/python/cpython/pull/22337
	# PSF License

	class GoodStrEnum(StrEnum):
		one = '1'
		two = '2'
		three = b'3', "ascii"
		four = b'4', "latin1", "strict"

	with pytest.raises(TypeError, match="1 is not a string"):

		class FirstFailedStrEnum(StrEnum):
			one = 1
			two = '2'

	with pytest.raises(TypeError, match="2 is not a string"):

		class SecondFailedStrEnum(StrEnum):
			one = '1'
			two = 2,
			three = '3'

	with pytest.raises(TypeError, match="2 is not a string"):

		class ThirdFailedStrEnum(StrEnum):
			one = '1'
			two = 2

	with pytest.raises(TypeError, match=f"encoding must be a string, not {sys.getdefaultencoding!r}"):

		class FourthFailedStrEnum(StrEnum):
			one = '1'
			two = b'2', sys.getdefaultencoding

	with pytest.raises(TypeError, match="errors must be a string, not 9"):

		class FifthFailedStrEnum(StrEnum):
			one = '1'
			two = b'2', "ascii", 9


@xfail_314
def test_member_dir_enum():

	class MyEnum(int, MemberDirEnum):
		apple = 1
		orange = 2

	if sys.version_info < (3, 11):
		assert dir(MyEnum) == ["__class__", "__doc__", "__members__", "__module__", "apple", "orange"]
	else:
		expected_dir = [
				"__abs__",
				"__add__",
				"__and__",
				"__bool__",
				"__ceil__",
				"__class__",
				"__contains__",
				"__delattr__",
				"__dir__",
				"__divmod__",
				"__doc__",
				"__eq__",
				"__float__",
				"__floor__",
				"__floordiv__",
				"__format__",
				"__ge__",
				"__getattribute__",
				"__getitem__",
				"__getnewargs__",
				"__getstate__",
				"__gt__",
				"__hash__",
				"__index__",
				"__init__",
				"__init_subclass__",
				"__int__",
				"__invert__",
				"__iter__",
				"__le__",
				"__len__",
				"__lshift__",
				"__lt__",
				"__members__",
				"__mod__",
				"__module__",
				"__mul__",
				"__name__",
				"__ne__",
				"__neg__",
				"__new__",
				"__or__",
				"__pos__",
				"__pow__",
				"__qualname__",
				"__radd__",
				"__rand__",
				"__rdivmod__",
				"__reduce__",
				"__reduce_ex__",
				"__repr__",
				"__rfloordiv__",
				"__rlshift__",
				"__rmod__",
				"__rmul__",
				"__ror__",
				"__round__",
				"__rpow__",
				"__rrshift__",
				"__rshift__",
				"__rsub__",
				"__rtruediv__",
				"__rxor__",
				"__setattr__",
				"__sizeof__",
				"__str__",
				"__sub__",
				"__subclasshook__",
				"__truediv__",
				"__trunc__",
				"__xor__",
				"apple",
				"as_integer_ratio",
				"bit_count",
				"bit_length",
				"conjugate",
				"denominator",
				"from_bytes",
				"imag",
				"numerator",
				"orange",
				"real",
				"to_bytes",
				]
		if sys.version_info > (3, 12):
			expected_dir.insert(79, "is_integer")
		assert dir(MyEnum) == expected_dir


def test_auto_number_enum():

	class MyEnum(AutoNumberEnum):
		apple = 1
		orange = 1

	assert MyEnum.apple._value_ == 1
	assert MyEnum.orange._value_ == 2


def test_ordered_enum():

	class MyEnum(OrderedEnum):
		apple = 1
		orange = 2
		strawberry = 0

	assert MyEnum.apple < MyEnum.orange
	assert MyEnum.apple <= MyEnum.orange
	assert MyEnum.apple > MyEnum.strawberry
	assert MyEnum.apple >= MyEnum.strawberry

	class MyEnum2(Enum):
		apple = 1
		orange = 2

	with pytest.raises(TypeError, match="'<' not supported between instances of 'MyEnum2' and 'MyEnum2'"):
		MyEnum2.apple < MyEnum2.orange  # type: ignore[operator]  # pylint: disable=pointless-statement
