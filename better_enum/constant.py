"""Python Advanced Enumerations & NameTuples"""
# stdlib
# From https://bitbucket.org/stoneleaf/aenum/src/default/aenum/__init__.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:

	class constant(object):
		"""
		Simple constant descriptor for NamedConstant and Enum use.
		"""

		def __init__(self, value, doc=None):
			self.value = value
			self.__doc__ = doc

	AutoValue = constant('autovalue', 'values are automatically created from _generate_next_value_')
	AutoNumber = constant('autonumber', 'integer value is prepended to members, beginning from START')
	MultiValue = constant('multivalue', 'each member can have several values')
	NoAlias = constant('noalias', 'duplicate valued members are distinct, not aliased')
	Unique = constant('unique', 'duplicate valued members are not allowed')

else:
	from aenum import constant, AutoValue, AutoNumber, MultiValue, NoAlias, Unique

__all__ = ["constant", "AutoValue", "AutoNumber", "MultiValue", "NoAlias", "Unique"]
