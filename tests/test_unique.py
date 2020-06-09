# -*- coding: utf-8 -*-

# stdlib
import sys
from unittest import TestCase

# this package
from better_enum import Enum, IntEnum, unique

pyver = float('%s.%s' % sys.version_info[:2])


class TestUnique(TestCase):
	"""2.4 doesn't allow class decorators, use function syntax."""

	def test_unique_clean(self):

		class Clean(Enum):
			one = 1
			two = 'dos'
			tres = 4.0

		unique(Clean)

		class Cleaner(IntEnum):
			single = 1
			double = 2
			triple = 3

		unique(Cleaner)

	def test_unique_dirty(self):
		try:

			class Dirty(Enum):
				__order__ = 'one two'
				one = 1
				two = 'dos'
				tres = 1

			unique(Dirty)
		except ValueError:
			exc = sys.exc_info()[1]
			message = exc.args[0]
		self.assertTrue('tres -> one' in message)

		try:

			class Dirtier(IntEnum):
				__order__ = 'single triple'
				single = 1
				double = 1
				triple = 3
				turkey = 3

			unique(Dirtier)
		except ValueError:
			exc = sys.exc_info()[1]
			message = exc.args[0]
		self.assertTrue('double -> single' in message)
		self.assertTrue('turkey -> triple' in message)

	def test_unique_with_name(self):

		@unique
		class Silly(Enum):
			one = 1
			two = 'dos'
			name = 3

		@unique
		class Sillier(IntEnum):
			single = 1
			name = 2
			triple = 3
			value = 4
