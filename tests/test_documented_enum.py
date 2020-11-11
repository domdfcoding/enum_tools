# stdlib
import math
from decimal import Decimal
from enum import Enum
from pathlib import Path

# 3rd party
import pytest

# this package
import enum_tools.documentation
from enum_tools.documentation import DocumentedEnum, document_enum

enum_tools.documentation.INTERACTIVE = True


@document_enum
class People(int, Enum):
	"""
	An enumeration of people
	"""

	Bob = bob = 1  # noqa  # doc: A person called Bob  # doc: another doc # isort: ignore
	Alice = 2  # doc: A person called Alice
	Carol = 3  # doc: A person called Carol

	@classmethod
	def iter_values(cls):
		return iter(cls)


# This is a dummy function to test mypy
def get_name(person: People = People.Bob) -> str:
	if person is People.Bob:
		return "Bob"
	elif person is People.Alice:
		return "Alice"
	elif person is People.Carol:
		return "Carol"
	return "Unknown"


def test_people():

	assert People.Bob == 1
	assert isinstance(People.Bob, People)
	assert isinstance(People.Bob, int)
	assert repr(People.Bob) == "<People.Bob: 1>"
	assert People.Bob.__doc__ == "A person called Bob"

	assert People.Alice == 2
	assert isinstance(People.Alice, People)
	assert isinstance(People.Alice, int)
	assert repr(People.Alice) == "<People.Alice: 2>"
	assert People.Alice.__doc__ == "A person called Alice"

	assert People.Carol == 3
	assert isinstance(People.Carol, People)
	assert isinstance(People.Carol, int)
	assert repr(People.Carol) == "<People.Carol: 3>"
	assert People.Carol.__doc__ == "A person called Carol"

	assert list(iter(People)) == [People.Bob, People.Alice, People.Carol]
	assert list(iter(People)) == [1, 2, 3]
	assert list(People.iter_values()) == [People.Bob, People.Alice, People.Carol]
	assert list(People.iter_values()) == [1, 2, 3]


class MyEnum(str, DocumentedEnum):
	a_value = b_value = "a value"  # doc: Docstring


def test_documented_enum():
	assert MyEnum.a_value == "a value"
	assert MyEnum.a_value.__doc__ == "Docstring"


@pytest.mark.parametrize(
		"obj",
		[
				pytest.param("abcdefg", id="string"),
				pytest.param(b"abcdefg", id="bytes"),
				b"\x00\x01",
				12345,
				123.45,
				Decimal(123.45),
				Path('.'),
				print,
				math.ceil,
				Path,
				Decimal,
				str,
				float,
				]
		)
def test_document_enum_wrong_types(obj):
	with pytest.raises(TypeError, match="'an_enum' must be an 'Enum', not .*!"):
		document_enum(obj)


@pytest.mark.parametrize(
		"obj",
		[
				pytest.param("abcdefg", id="string"),
				pytest.param(b"abcdefg", id="bytes"),
				b"\x00\x01",
				12345,
				123.45,
				Decimal(123.45),
				Path('.'),
				print,
				math.ceil,
				Path,
				Decimal,
				str,
				float,
				]
		)
def test_document_member_wrong_types(obj):
	with pytest.raises(TypeError, match="'an_enum' must be an 'Enum', not .*!"):
		enum_tools.document_member(obj)


def test_document_enum_not_interactive():
	interactive_last_value = enum_tools.documentation.INTERACTIVE

	enum_tools.documentation.INTERACTIVE = False

	@document_enum
	class People(int, Enum):
		"""
		An enumeration of people
		"""

		Bob = bob = 1  # noqa  # doc: A person called Bob  # doc: another doc # isort: ignore
		Alice = 2  # doc: A person called Alice
		Carol = 3  # doc: A person called Carol

		@classmethod
		def iter_values(cls):
			return iter(cls)

	assert People.Bob == 1
	assert isinstance(People.Bob, People)
	assert isinstance(People.Bob, int)
	assert repr(People.Bob) == "<People.Bob: 1>"
	assert People.Bob.__doc__ == "\n\t\tAn enumeration of people\n\t\t"  # The default

	assert People.Alice == 2
	assert isinstance(People.Alice, People)
	assert isinstance(People.Alice, int)
	assert repr(People.Alice) == "<People.Alice: 2>"
	assert People.Alice.__doc__ == "\n\t\tAn enumeration of people\n\t\t"  # The default

	assert People.Carol == 3
	assert isinstance(People.Carol, People)
	assert isinstance(People.Carol, int)
	assert repr(People.Carol) == "<People.Carol: 3>"
	assert People.Carol.__doc__ == "\n\t\tAn enumeration of people\n\t\t"  # The default

	assert list(iter(People)) == [People.Bob, People.Alice, People.Carol]
	assert list(iter(People)) == [1, 2, 3]
	assert list(People.iter_values()) == [People.Bob, People.Alice, People.Carol]
	assert list(People.iter_values()) == [1, 2, 3]

	enum_tools.documentation.INTERACTIVE = interactive_last_value
