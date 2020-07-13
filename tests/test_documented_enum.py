# stdlib
from enum import Enum

# this package
from enum_tools.decorator import DocumentedEnum, document_enum


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
	return 'Unknown'


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
