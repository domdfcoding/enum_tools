# -*- coding: utf-8 -*-

# this package
from better_enum import Enum, NamedTuple, StrEnum


class IntStooges(int, Enum):
	LARRY = 1
	CURLY = 2
	MOE = 3


class Name(StrEnum):
	BDFL = 'Guido van Rossum'
	FLUFL = 'Barry Warsaw'


LifeForm = NamedTuple('LifeForm', 'branch genus species', module=__name__)  # type: ignore


class DeathForm(NamedTuple):
	color: int = 0
	rigidity: int = 1
	odor: int = 2


class WhatsIt(NamedTuple):

	def what(self):
		return self[0]


class ThatsIt(WhatsIt):
	blah = 0
	bleh = 1
