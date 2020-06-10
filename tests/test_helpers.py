#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  demo_classes.py
#
#  Based on aenum
#  https://bitbucket.org/stoneleaf/aenum
#  Copyright (c) 2015, 2016, 2017, 2018 Ethan Furman.
#  All rights reserved.
#  Licensed under the 3-clause BSD License:
#  |  Redistribution and use in source and binary forms, with or without
#  |  modification, are permitted provided that the following conditions
#  |  are met:
#  |
#  |      Redistributions of source code must retain the above
#  |      copyright notice, this list of conditions and the
#  |      following disclaimer.
#  |
#  |      Redistributions in binary form must reproduce the above
#  |      copyright notice, this list of conditions and the following
#  |      disclaimer in the documentation and/or other materials
#  |      provided with the distribution.
#  |
#  |      Neither the name Ethan Furman nor the names of any
#  |      contributors may be used to endorse or promote products
#  |      derived from this software without specific prior written
#  |      permission.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  |  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  |  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  |  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  |  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  |  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  |  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  |  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  |  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  |  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  |  POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
from operator import abs as _abs_
from operator import add as _add_
from operator import and_ as _and_
from operator import floordiv as _floordiv_
from operator import inv as _inv_
from operator import lshift as _lshift_
from operator import mod as _mod_
from operator import mul as _mul_
from operator import neg as _neg_
from operator import or_ as _or_
from operator import pos as _pos_
from operator import pow as _pow_
from operator import rshift as _rshift_
from operator import sub as _sub_
from operator import truediv as _truediv_
from operator import xor as _xor_
from unittest import TestCase

# 3rd party
from aenum import auto  # type: ignore

# this package
from better_enum import constant
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
				assert value.value, final == f"{op.__name__} {first!r} -> {value!r} != {final!r}"
			else:
				left = first
				right = auto()
				value = op(left, right)
				right.value = second
				self.assertEqual(
						value.value,
						final,
						f"forward: {first!r} {op.__name__} {second!r} -> {value.value!r} != {final!r}"
						)
				left = auto()
				right = second
				value = op(left, right)
				left.value = first
				self.assertEqual(
						value.value,
						final,
						f"reversed: {second!r} {op.__name__} {first!r} -> {value.value!r} != {final!r}"
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
		assert value.value == 'I see 17 %s!' % 'eggs'

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
			assert False
