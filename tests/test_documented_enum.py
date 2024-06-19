# stdlib
import math
import sys
import warnings
from decimal import Decimal
from enum import Enum
from pathlib import Path

# 3rd party
import pytest

# this package
import enum_tools.documentation
from enum_tools.documentation import DocumentedEnum, MultipleDocstringsWarning, document_enum

enum_tools.documentation.INTERACTIVE = True
NEW_ENUM_REPR = sys.version_info >= (3, 14)

xfail_314 = pytest.mark.xfail(
		reason="Python 3.14 behaviour has not been finalised yet.",
		condition=sys.version_info[:2] == (3, 14) and sys.version_info.releaselevel == "alpha"
		)


@document_enum
class People(int, Enum):
	"""
	An enumeration of people
	"""

	Bob = bob = 1  # noqa  # doc: A person called Bob  # doc: another doc # isort: ignore
	Alice = 2  # doc: A person called Alice
	Carol = 3
	"""
	A person called Carol.

	This is a multiline docstring.
	"""

	@classmethod
	def iter_values(cls):  # noqa: MAN002
		return iter(cls)

	#: A person called Dennis

	Dennis = 4


# This is a dummy function to test mypy
def get_name(person: People = People.Bob) -> str:
	if person is People.Bob:
		return "Bob"
	elif person is People.Alice:
		return "Alice"
	elif person is People.Carol:
		return "Carol"
	return "Unknown"


@xfail_314
def test_people():

	assert People.Bob == 1
	assert isinstance(People.Bob, People)
	assert isinstance(People.Bob, int)
	assert repr(People.Bob) == "People.Bob" if NEW_ENUM_REPR else "<People.Bob: 1>"
	assert People.Bob.__doc__ == "A person called Bob"

	assert People.Alice == 2
	assert isinstance(People.Alice, People)
	assert isinstance(People.Alice, int)
	assert repr(People.Alice) == "People.Alice" if NEW_ENUM_REPR else "<People.Alice: 2>"
	assert People.Alice.__doc__ == "A person called Alice"

	assert People.Carol == 3
	assert isinstance(People.Carol, People)
	assert isinstance(People.Carol, int)
	assert repr(People.Carol) == "People.Carol" if NEW_ENUM_REPR else "<People.Carol: 3>"
	assert People.Carol.__doc__ == "A person called Carol.\n\nThis is a multiline docstring."

	assert People.Dennis == 4
	assert isinstance(People.Dennis, People)
	assert isinstance(People.Dennis, int)
	assert repr(People.Dennis) == "People.Dennis" if NEW_ENUM_REPR else "<People.Dennis: 4>"
	assert People.Dennis.__doc__ == "A person called Dennis"

	assert list(iter(People)) == [People.Bob, People.Alice, People.Carol, People.Dennis]
	assert list(iter(People)) == [1, 2, 3, 4]
	assert list(People.iter_values()) == [People.Bob, People.Alice, People.Carol, People.Dennis]
	assert list(People.iter_values()) == [1, 2, 3, 4]


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
def test_document_enum_wrong_types(obj: object):
	with pytest.raises(TypeError, match="'an_enum' must be an 'Enum', not .*!"):
		document_enum(obj)  # type: ignore[type-var]


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
def test_document_member_wrong_types(obj: object):
	with pytest.raises(TypeError, match="'an_enum' must be an 'Enum', not .*!"):
		enum_tools.document_member(obj)  # type: ignore[arg-type]


@xfail_314
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
		def iter_values(cls):  # noqa: MAN002
			return iter(cls)

	assert People.Bob == 1
	assert isinstance(People.Bob, People)
	assert isinstance(People.Bob, int)
	assert repr(People.Bob) == "People.Bob" if NEW_ENUM_REPR else "<People.Bob: 1>"
	assert People.Bob.__doc__ == "\n\t\tAn enumeration of people\n\t\t"  # The default

	assert People.Alice == 2
	assert isinstance(People.Alice, People)
	assert isinstance(People.Alice, int)
	assert repr(People.Alice) == "People.Alice" if NEW_ENUM_REPR else "<People.Alice: 2>"
	assert People.Alice.__doc__ == "\n\t\tAn enumeration of people\n\t\t"  # The default

	assert People.Carol == 3
	assert isinstance(People.Carol, People)
	assert isinstance(People.Carol, int)
	assert repr(People.Carol) == "People.Carol" if NEW_ENUM_REPR else "<People.Carol: 3>"
	assert People.Carol.__doc__ == "\n\t\tAn enumeration of people\n\t\t"  # The default

	assert list(iter(People)) == [People.Bob, People.Alice, People.Carol]
	assert list(iter(People)) == [1, 2, 3]
	assert list(People.iter_values()) == [People.Bob, People.Alice, People.Carol]
	assert list(People.iter_values()) == [1, 2, 3]

	enum_tools.documentation.INTERACTIVE = interactive_last_value


@xfail_314
# yapf: disable
def test_multiple_docstring_warning():
	with pytest.warns(UserWarning) as record:

		@document_enum
		class ModeOfTransport(Enum):
			feeder = "feeder"  # doc: A feeder vessel is a rather small vessel sent by a ship operator and moves in the region

			"""A deep sea vessel is a rather large vessel sent by a ship operator and moves between distant regions, e.g.
			continents."""
			deep_sea_vessel = "deep_sea_vessel"

# yapf: enable

	assert len(record) == 1
	warningmsg: warnings.WarningMessage = record[0]
	assert isinstance(warningmsg.message, MultipleDocstringsWarning)
	assert warningmsg.message.member is ModeOfTransport.feeder
	assert warningmsg.message.docstrings == [
			"A deep sea vessel is a rather large vessel sent by a ship operator and moves between distant regions, "
			"e.g.\ncontinents.",
			"A feeder vessel is a rather small vessel sent by a ship operator and moves in the region",
			]

	# Strictly this is indeterminate and the order shouldn't be relied on;
	# it's an implementation detail that the priority is what it is
	assert ModeOfTransport.feeder.__doc__ == (
			"A deep sea vessel is a rather large vessel sent by a ship operator and moves between distant regions, "
			"e.g.\ncontinents."
			)

	if sys.version_info >= (3, 11):
		# 3.11 changed this to None instead of a placeholder
		assert ModeOfTransport.deep_sea_vessel.__doc__ is None
	else:
		assert ModeOfTransport.deep_sea_vessel.__doc__ == "An enumeration."
