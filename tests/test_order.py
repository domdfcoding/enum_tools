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

# this package
from better_enum import Enum


def test_same_members():

	class Color(Enum):
		_order_ = 'red green blue'
		red = 1
		green = 2
		blue = 3


def test_same_members_with_aliases():

	class Color(Enum):
		_order_ = 'red green blue'
		red = 1
		green = 2
		blue = 3
		verde = green


class TestOrder(TestCase):

	def test_same_members_wrong_order(self):
		with self.assertRaisesRegex(TypeError, 'member order does not match _order_'):

			class Color(Enum):
				_order_ = 'red green blue'
				red = 1
				blue = 3
				green = 2

	def test_order_has_extra_members(self):
		with self.assertRaisesRegex(TypeError, 'member order does not match _order_'):

			class Color(Enum):
				_order_ = 'red green blue purple'
				red = 1
				green = 2
				blue = 3

	def test_order_has_extra_members_with_aliases(self):
		with self.assertRaisesRegex(TypeError, 'member order does not match _order_'):

			class Color(Enum):
				_order_ = 'red green blue purple'
				red = 1
				green = 2
				blue = 3
				verde = green

	def test_enum_has_extra_members(self):
		with self.assertRaisesRegex(TypeError, 'member order does not match _order_'):

			class Color(Enum):
				_order_ = 'red green blue'
				red = 1
				green = 2
				blue = 3
				purple = 4

	def test_enum_has_extra_members_with_aliases(self):
		with self.assertRaisesRegex(TypeError, 'member order does not match _order_'):

			class Color(Enum):
				_order_ = 'red green blue'
				red = 1
				green = 2
				blue = 3
				purple = 4
				verde = green
