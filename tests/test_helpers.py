# -*- coding: utf-8 -*-

# stdlib
from operator import (
	abs as _abs_, add as _add_, and_ as _and_, floordiv as _floordiv_, inv as _inv_,
	lshift as _lshift_, mod as _mod_, mul as _mul_, neg as _neg_, or_ as _or_, pos as _pos_, pow as _pow_,
	rshift as _rshift_, sub as _sub_, truediv as _truediv_, xor as _xor_,
	)
from unittest import TestCase

# 3rd party
from aenum import (auto)  # type: ignore

# this package
from better_enum import (
	constant,
	)
from better_enum.utils import _is_descriptor, _is_dunder, _is_sunder


class TestHelpers(TestCase):
	# _is_descriptor, _is_sunder, _is_dunder

	def test_is_descriptor(self):

		class Foo:
			pass

		for attr in ('__get__', '__set__', '__delete__'):
			obj = Foo()
			self.assertFalse(_is_descriptor(obj))
			setattr(obj, attr, 1)
			self.assertTrue(_is_descriptor(obj))

	def test_is_sunder(self):
		for s in ('_a_', '_aa_'):
			self.assertTrue(_is_sunder(s))

		for s in (
				'a',
				'a_',
				'_a',
				'__a',
				'a__',
				'__a__',
				'_a__',
				'__a_',
				'_',
				'__',
				'___',
				'____',
				'_____',
				):
			self.assertFalse(_is_sunder(s))

	def test_is_dunder(self):
		for s in ('__a__', '__aa__'):
			self.assertTrue(_is_dunder(s))
		for s in (
				'a',
				'a_',
				'_a',
				'__a',
				'a__',
				'_a_',
				'_a__',
				'__a_',
				'_',
				'__',
				'___',
				'____',
				'_____',
				):
			self.assertFalse(_is_dunder(s))

	def test_auto(self):

		def tester(first, op, final, second=None):
			if second is None:
				left = auto()
				value = op(left)
				left.value = first
				self.assertEqual(value.value, final, "%s %r -> %r != %r" % (op.__name__, first, value, final))
			else:
				left = first
				right = auto()
				value = op(left, right)
				right.value = second
				self.assertEqual(
						value.value,
						final,
						"forward: %r %s %r -> %r != %r" % (first, op.__name__, second, value.value, final)
						)
				left = auto()
				right = second
				value = op(left, right)
				left.value = first
				self.assertEqual(
						value.value,
						final,
						"reversed: %r %s %r -> %r != %r" % (second, op.__name__, first, value.value, final)
						)

		for args in (
				(1, _abs_, abs(1)),
				(-3, _abs_, abs(-3)),
				(1, _add_, 1 + 2, 2),
				(25, _floordiv_, 25 // 5, 5),
				(49, _truediv_, 49 / 9, 9),
				(6, _mod_, 6 % 9, 9),
				(5, _lshift_, 5 << 2, 2),
				(5, _rshift_, 5 >> 2, 2),
				(3, _mul_, 3 * 6, 6),
				(5, _neg_, -5),
				(-4, _pos_, +(-4)),
				(2, _pow_, 2**5, 5),
				(7, _sub_, 7 - 10, 10),
				(1, _or_, 1 | 2, 2),
				(3, _xor_, 3 ^ 6, 6),
				(3, _and_, 3 & 6, 6),
				(7, _inv_, ~7),
				('a', _add_, 'a' + 'b', 'b'),
				('a', _mul_, 'a' * 3, 3),
				):
			tester(*args)

		# strings are a pain
		left = auto()
		right = 'eggs'
		value = _mod_(left, right)
		left.value = 'I see 17 %s!'
		self.assertEqual(value.value, 'I see 17 %s!' % 'eggs')

	def test_constant(self):
		errors = []

		def tester(first, op, final, second=None):
			if second is None:
				primary = constant(first)
				secondary = constant(op(primary))
				if secondary.value != final:
					errors.append("%s %r -> %r != %r" % (op.__name__, first, secondary.value, final), )
			else:
				left = constant(first)
				right = second
				value = op(left, right)
				if value != final:
					errors.append("forward: %r %s %r -> %r != %r" % (first, op.__name__, second, value, final), )
				left = first
				right = constant(second)
				value = op(left, right)
				if value != final:
					errors.append("reversed: %r %s %r -> %r != %r" % (second, op.__name__, first, value, final), )

		for args in (
				(1, _abs_, abs(1)),
				(-3, _abs_, abs(-3)),
				(1, _add_, 1 + 2, 2),
				(25, _floordiv_, 25 // 5, 5),
				(49, _truediv_, 49 / 9, 9),
				(6, _mod_, 6 % 9, 9),
				(5, _lshift_, 5 << 2, 2),
				(5, _rshift_, 5 >> 2, 2),
				(3, _mul_, 3 * 6, 6),
				(5, _neg_, -5),
				(-4, _pos_, +(-4)),
				(2, _pow_, 2**5, 5),
				(7, _sub_, 7 - 10, 10),
				(1, _or_, 1 | 2, 2),
				(3, _xor_, 3 ^ 6, 6),
				(3, _and_, 3 & 6, 6),
				(7, _inv_, ~7),
				('a', _add_, 'a' + 'b', 'b'),
				('a', _mul_, 'a' * 3, 3),
				):
			tester(*args)

		# strings are a pain
		left = constant('I see 17 %s!')
		right = 'eggs'
		value = _mod_(left, right)
		if value != 'I see 17 %s!' % 'eggs':
			errors.append("'I see 17 eggs!' != %r" % value)
		if errors:
			print()
			for error in errors:
				print(error)
			self.assertTrue(False)
