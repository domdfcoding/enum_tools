"""
Import Enum etc. from the correct place, depending on whether mypy is running or not
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from enum import Enum, unique, Flag, IntFlag, EnumMeta
	from typing import NamedTuple, TYPE_CHECKING
else:
	from aenum import Enum, NamedTuple, unique, Flag, IntFlag, EnumMeta

__all__ = ["Enum", "NamedTuple", "unique", "Flag", "IntFlag", "EnumMeta"]
