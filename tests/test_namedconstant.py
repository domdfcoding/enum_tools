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
from unittest import TestCase

# 3rd party
from aenum import NamedConstant  # type: ignore

# this package
from better_enum import constant


class TestNamedConstant(TestCase):

	def test_constantness(self):

		class K(NamedConstant):
			PI = 3.141596
			TAU = 2 * PI

		assert K.PI == 3.141596
		assert K.TAU == 2 * K.PI
		with self.assertRaisesRegex(AttributeError, 'cannot rebind constant'):
			K.PI = 9
		with self.assertRaisesRegex(AttributeError, 'cannot delete constant'):
			del K.PI
		with self.assertRaisesRegex(AttributeError, 'cannot rebind constant'):
			K('PI', 3)


def test_duplicates():

	class CardNumber(NamedConstant):
		ACE = 11
		TWO = 2
		THREE = 3
		FOUR = 4
		FIVE = 5
		SIX = 6
		SEVEN = 7
		EIGHT = 8
		NINE = 9
		TEN = 10
		JACK = 10
		QUEEN = 10
		KING = 10

	assert CardNumber.TEN is not CardNumber.JACK
	assert CardNumber.TEN == CardNumber.JACK
	assert CardNumber.TEN == 10


def test_extend_constants():

	class CardSuit(NamedConstant):
		HEARTS = 1
		SPADES = 2
		DIAMONTS = 3
		CLUBS = 4

	assert CardSuit.HEARTS == 1
	stars = CardSuit('STARS', 5)
	assert stars is CardSuit.STARS
	assert CardSuit.STARS == 5


def test_constant_with_docstring():

	class Stuff(NamedConstant):
		Artifact = constant(7, "lucky number!")
		Bowling = 11
		HillWomp = constant(29, 'blah blah')

	assert Stuff.Artifact == 7
	assert Stuff.Artifact.__doc__ == 'lucky number!'
	assert Stuff.Bowling == 11
	assert Stuff.Bowling.__doc__ is None
	assert Stuff.HillWomp == 29
	assert Stuff.HillWomp.__doc__ == 'blah blah'
