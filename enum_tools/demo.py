# stdlib
from enum import Enum
from typing import List

# this package
import enum_tools.documentation
from enum_tools.documentation import document_enum

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
		"""
		Iterate over the values of the Enum.
		"""

		return iter(cls)

	@classmethod
	def as_list(cls) -> List:
		"""
		Return the Enum's members as a list.
		"""

		return list(cls)


@document_enum
class NoMethods(int, Enum):
	"""
	An enumeration of people without any methods.
	"""

	Bob = bob = 1  # noqa  # doc: A person called Bob  # doc: another doc # isort: ignore
	Alice = 2  # doc: A person called Alice
	Carol = 3  # doc: A person called Carol
