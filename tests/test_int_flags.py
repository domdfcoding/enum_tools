#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_int_flags.py
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
import sys
import threading
import unittest
from collections import OrderedDict
from unittest import TestCase

# 3rd party
import pytest  # type: ignore
from aenum import auto  # type: ignore

# this package
from better_enum import IntFlag

pyver = float('%s.%s' % sys.version_info[:2])


class Perm(IntFlag):
	X = 1 << 0
	W = 1 << 1
	R = 1 << 2


class Color(IntFlag):
	BLACK = 0
	RED = 1
	GREEN = 2
	BLUE = 4
	PURPLE = RED | BLUE


class Open(IntFlag):
	"not a good flag candidate"
	RO = 0
	WO = 1
	RW = 2
	AC = 3
	CE = 1 << 19


class TestIntFlag(TestCase):
	"""Tests of the IntFlags."""

	def test_membership(self):

		self.assertRaises(TypeError, lambda: 'GREEN' in Color)
		self.assertRaises(TypeError, lambda: 'RW' in Open)
		assert Color.GREEN in Color
		assert Open.RW in Open
		self.assertFalse(Color.GREEN in Open)
		self.assertFalse(Open.RW in Color)
		self.assertRaises(TypeError, lambda: 2 in Color)
		self.assertRaises(TypeError, lambda: 2 in Open)

	def test_member_contains(self):

		self.assertRaises(TypeError, lambda: 'test' in Color.RED)
		self.assertRaises(TypeError, lambda: 1 in Color.RED)
		assert Color.RED in Color.RED
		assert Color.RED in Color.PURPLE

	def test_name_lookup(self):

		assert Color.RED is Color['RED']
		assert Color.RED | Color.GREEN is Color['RED|GREEN']
		assert Color.PURPLE is Color['RED|BLUE']

	def test_type(self):

		for f in Perm:
			assert isinstance(f, Perm)
			assert f == f.value
		assert isinstance(Perm.W | Perm.X, Perm)
		assert Perm.W | Perm.X == 3
		for f in Open:
			assert isinstance(f, Open)
			assert f == f.value
		assert isinstance(Open.WO | Open.RW, Open)
		assert Open.WO | Open.RW == 3

	def test_str(self):

		assert str(Perm.R) == 'Perm.R'
		assert str(Perm.W) == 'Perm.W'
		assert str(Perm.X) == 'Perm.X'
		assert str(Perm.R | Perm.W) == 'Perm.R|W'
		assert str(Perm.R | Perm.W | Perm.X) == 'Perm.R|W|X'
		assert str(Perm.R | 8) == 'Perm.8|R'
		assert str(Perm(0)) == 'Perm.0'
		assert str(Perm(8)) == 'Perm.8'
		assert str(~Perm.R) == 'Perm.W|X'
		assert str(~Perm.W) == 'Perm.R|X'
		assert str(~Perm.X) == 'Perm.R|W'
		assert str(~(Perm.R | Perm.W)) == 'Perm.X'
		assert str(~(Perm.R | Perm.W | Perm.X)) == 'Perm.-8'
		assert str(~(Perm.R | 8)) == 'Perm.W|X'
		assert str(Perm(~0)) == 'Perm.R|W|X'
		assert str(Perm(~8)) == 'Perm.R|W|X'

		assert str(Open.RO) == 'Open.RO'
		assert str(Open.WO) == 'Open.WO'
		assert str(Open.AC) == 'Open.AC'
		assert str(Open.RO | Open.CE) == 'Open.CE'
		assert str(Open.WO | Open.CE) == 'Open.CE|WO'
		assert str(Open(4)) == 'Open.4'
		assert str(~Open.RO) == 'Open.CE|AC|RW|WO'
		assert str(~Open.WO) == 'Open.CE|RW'
		assert str(~Open.AC) == 'Open.CE'
		assert str(~(Open.RO | Open.CE)) == 'Open.AC|RW|WO'
		assert str(~(Open.WO | Open.CE)) == 'Open.RW'
		assert str(Open(~4)) == 'Open.CE|AC|RW|WO'

	def test_repr(self):

		assert repr(Perm.R) == '<Perm.R: 4>'
		assert repr(Perm.W) == '<Perm.W: 2>'
		assert repr(Perm.X) == '<Perm.X: 1>'
		assert repr(Perm.R | Perm.W) == '<Perm.R|W: 6>'
		assert repr(Perm.R | Perm.W | Perm.X) == '<Perm.R|W|X: 7>'
		assert repr(Perm.R | 8) == '<Perm.8|R: 12>'
		assert repr(Perm(0)) == '<Perm.0: 0>'
		assert repr(Perm(8)) == '<Perm.8: 8>'
		assert repr(~Perm.R) == '<Perm.W|X: -5>'
		assert repr(~Perm.W) == '<Perm.R|X: -3>'
		assert repr(~Perm.X) == '<Perm.R|W: -2>'
		assert repr(~(Perm.R | Perm.W)) == '<Perm.X: -7>'
		assert repr(~(Perm.R | Perm.W | Perm.X)) == '<Perm.-8: -8>'
		assert repr(~(Perm.R | 8)) == '<Perm.W|X: -13>'
		assert repr(Perm(~0)) == '<Perm.R|W|X: -1>'
		assert repr(Perm(~8)) == '<Perm.R|W|X: -9>'

		assert repr(Open.RO) == '<Open.RO: 0>'
		assert repr(Open.WO) == '<Open.WO: 1>'
		assert repr(Open.AC) == '<Open.AC: 3>'
		assert repr(Open.RO | Open.CE) == '<Open.CE: 524288>'
		assert repr(Open.WO | Open.CE) == '<Open.CE|WO: 524289>'
		assert repr(Open(4)) == '<Open.4: 4>'
		assert repr(~Open.RO) == '<Open.CE|AC|RW|WO: -1>'
		assert repr(~Open.WO) == '<Open.CE|RW: -2>'
		assert repr(~Open.AC) == '<Open.CE: -4>'
		assert repr(~(Open.RO | Open.CE)) == '<Open.AC|RW|WO: -524289>'
		assert repr(~(Open.WO | Open.CE)) == '<Open.RW: -524290>'
		assert repr(Open(~4)) == '<Open.CE|AC|RW|WO: -5>'

	def test_or(self):

		for i in Perm:
			for j in Perm:
				assert i | j == i.value | j.value
				assert (i | j).value == i.value | j.value
				assert isinstance(i | j, Perm)
			for j in range(8):
				assert i | j == i.value | j
				assert (i | j).value == i.value | j
				assert isinstance(i | j, Perm)
				assert j | i == j | i.value
				assert (j | i).value == j | i.value
				assert isinstance(j | i, Perm)
		for i in Perm:
			self.assertIs(i | i, i)
			self.assertIs(i | 0, i)
			self.assertIs(0 | i, i)

		self.assertIs(Open.RO | Open.CE, Open.CE)

	def test_and(self):

		RW = Perm.R | Perm.W
		RX = Perm.R | Perm.X
		WX = Perm.W | Perm.X
		RWX = Perm.R | Perm.W | Perm.X
		values = list(Perm) + [RW, RX, WX, RWX, Perm(0)]
		for i in values:
			for j in values:
				self.assertEqual(i & j, i.value & j.value, f'i is {i!r}, j is {j!r}')
				self.assertEqual((i & j).value, i.value & j.value, f'i is {i!r}, j is {j!r}')
				assert type(i & j), Perm is f'i is {i!r}, j is {j!r}'
			for j in range(8):
				assert i & j == i.value & j
				assert (i & j).value == i.value & j
				assert isinstance(i & j, Perm)
				assert j & i == j & i.value
				assert (j & i).value == j & i.value
				assert isinstance(j & i, Perm)
		for i in Perm:
			assert i & i is i
			assert i & 7 is i
			assert 7 & i is i

		assert Open.RO & Open.CE is Open.RO

	def test_xor(self):

		for i in Perm:
			for j in Perm:
				assert i ^ j == i.value ^ j.value
				assert (i ^ j).value == i.value ^ j.value
				assert isinstance(i ^ j, Perm)
			for j in range(8):
				assert i ^ j == i.value ^ j
				assert (i ^ j).value == i.value ^ j
				assert isinstance(i ^ j, Perm)
				assert j ^ i == j ^ i.value
				assert (j ^ i).value == j ^ i.value
				assert isinstance(j ^ i, Perm)
		for i in Perm:
			self.assertIs(i ^ 0, i)
			self.assertIs(0 ^ i, i)

		assert Open.RO ^ Open.CE is Open.CE
		assert Open.CE ^ Open.CE is Open.RO

	def test_invert(self):

		RW = Perm.R | Perm.W
		RX = Perm.R | Perm.X
		WX = Perm.W | Perm.X
		RWX = Perm.R | Perm.W | Perm.X
		values = list(Perm) + [RW, RX, WX, RWX, Perm(0)]
		for i in values:
			assert ~i == ~i.value
			assert (~i).value == ~i.value
			assert isinstance(~i, Perm)
			assert ~~i == i
		for i in Perm:
			assert ~~i is i

		assert Open.WO & ~Open.WO is Open.RO
		assert (Open.WO | Open.CE) & ~Open.WO is Open.CE

	def test_iter(self):

		NoPerm = Perm.R ^ Perm.R
		RWX = Perm.R | Perm.W | Perm.X
		assert list(NoPerm) == []
		assert list(Perm.R) == [Perm.R]
		assert list(RWX), [Perm.R, Perm.W == Perm.X]

	def test_programatic_function_string(self):
		Perm = IntFlag('Perm', 'R W X')
		lst = list(Perm)
		assert len(lst) == len(Perm)
		self.assertEqual(len(Perm), 3, Perm)
		assert lst, [Perm.R, Perm.W == Perm.X]
		for i, n in enumerate('R W X'.split()):
			v = 1 << i
			e = Perm(v)
			assert e.value == v
			assert isinstance(e.value, int)
			assert e == v
			assert e.name == n
			assert e in Perm
			assert isinstance(e, Perm)

	def test_programatic_function_string_with_start(self):
		Perm = IntFlag('Perm', 'R W X', start=8)
		lst = list(Perm)
		assert len(lst) == len(Perm)
		self.assertEqual(len(Perm), 3, Perm)
		assert lst, [Perm.R, Perm.W == Perm.X]
		for i, n in enumerate('R W X'.split()):
			v = 8 << i
			e = Perm(v)
			assert e.value == v
			assert isinstance(e.value, int)
			assert e == v
			assert e.name == n
			assert e in Perm
			assert isinstance(e, Perm)

	def test_programatic_function_string_list(self):
		Perm = IntFlag('Perm', ['R', 'W', 'X'])
		lst = list(Perm)
		assert len(lst) == len(Perm)
		self.assertEqual(len(Perm), 3, Perm)
		assert lst, [Perm.R, Perm.W == Perm.X]
		for i, n in enumerate('R W X'.split()):
			v = 1 << i
			e = Perm(v)
			assert e.value == v
			assert isinstance(e.value, int)
			assert e == v
			assert e.name == n
			assert e in Perm
			assert isinstance(e, Perm)

	def test_programatic_function_iterable(self):
		Perm = IntFlag('Perm', (('R', 2), ('W', 8), ('X', 32)))
		lst = list(Perm)

		assert len(lst) == len(Perm)
		self.assertEqual(len(Perm), 3, Perm)
		assert lst, [Perm.R, Perm.W == Perm.X]

		for i, n in enumerate('R W X'.split()):
			v = 1 << (2 * i + 1)
			e = Perm(v)
			assert e.value == v
			assert isinstance(e.value, int)
			assert e == v
			assert e.name == n
			assert e in Perm
			assert isinstance(e, Perm)

	def test_programatic_function_from_dict(self):
		Perm = IntFlag('Perm', OrderedDict((('R', 2), ('W', 8), ('X', 32))))
		lst = list(Perm)

		assert len(lst) == len(Perm)
		self.assertEqual(len(Perm), 3, Perm)
		assert lst, [Perm.R, Perm.W == Perm.X]

		for i, n in enumerate('R W X'.split()):
			v = 1 << (2 * i + 1)
			e = Perm(v)
			assert e.value == v
			assert isinstance(e.value, int)
			assert e == v
			assert e.name == n
			assert e in Perm
			assert isinstance(e, Perm)

	def test_containment(self):

		R, W, X = Perm
		RW = R | W
		RX = R | X
		WX = W | X
		RWX = R | W | X

		assert R in RW
		assert R in RX
		assert R in RWX
		assert W in RW
		assert W in WX
		assert W in RWX
		assert X in RX
		assert X in WX
		assert X in RWX
		assert R not in WX
		assert W not in RX
		assert X not in RW

	def test_bool(self):

		for f in Perm:
			assert f

		for f in Open:
			assert bool(f.value) == bool(f)

	@unittest.skipUnless(threading, 'Threading required for this test.')
	def test_unique_composite(self):
		# override __eq__ to be identity only
		class TestFlag(IntFlag):
			_order_ = 'one two three four five six seven eight'
			one = auto()
			two = auto()
			three = auto()
			four = auto()
			five = auto()
			six = auto()
			seven = auto()
			eight = auto()

			def __eq__(self, other):
				return self is other

			def __hash__(self):
				return hash(self._value_)

		# have multiple threads competing to complete the composite members
		seen = set()
		failed = [False]

		def cycle_enum():
			# nonlocal failed
			try:
				for i in range(256):
					seen.add(TestFlag(i))
			except Exception:
				failed[0] = True

		threads = [threading.Thread(target=cycle_enum) for _ in range(8)]
		for t in threads:
			t.start()
		for t in threads:
			t.join()
		# check that only 248 members were created (8 were created originally)
		self.assertFalse(failed[0], 'at least one thread failed while creating composite members')
		assert 256, len(seen) == 'too many composite members created'
