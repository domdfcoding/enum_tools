"""
test_enums
~~~~~~~~~~~~~~~
"""

# this package
from enum_tools import IntEnum, StrEnum


class DramatisPersonae(StrEnum):
	Message = "a secret message"
	Bob = "The sender"
	Alice = "The recipient"
	Chuck = "A man of malicious intent"
	Craig = "A password cracker"
	Eve = "An eavesdropper"


def test_str_enum():
	assert DramatisPersonae.Message == "a secret message"
	assert DramatisPersonae.Alice != "An eavesdropper"
	assert str(DramatisPersonae.Craig) == "A password cracker"
	assert DramatisPersonae("The sender") == DramatisPersonae.Bob == "The sender"
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
