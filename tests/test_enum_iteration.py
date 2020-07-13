#!/usr/bin/env python3
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
import os
from collections import OrderedDict
from datetime import timedelta
from enum import Enum as StdlibEnum
from enum import EnumMeta as StdlibEnumMeta
from unittest import TestCase

# 3rd party
import pytest
from aenum import EnumMeta, _decompose, _high_bit, auto, enum, extend_enum, skip  # type: ignore

# this package
from better_enum import (
		AutoEnum,
		AutoNumber,
		AutoNumberEnum,
		AutoValue,
		Enum,
		Flag,
		IntEnum,
		MultiValue,
		MultiValueEnum,
		NoAlias,
		OrderedEnum,
		Unique,
		UniqueEnum,
		constant
		)
from better_enum.utils import _is_sunder
from tests.conftest import tempdir
from tests.demo_classes import IntStooges, Name


def test_iteration_order():

	class Season(Enum):
		__order__ = 'SUMMER WINTER AUTUMN SPRING'
		SUMMER = 2
		WINTER = 4
		AUTUMN = 3
		SPRING = 1

	assert list(Season) == [Season.SUMMER, Season.WINTER, Season.AUTUMN, Season.SPRING]


def test_iteration_order_with_unorderable_values():

	class Complex(Enum):
		a = complex(7, 9)
		b = complex(3.14, 2)
		c = complex(1, -1)
		d = complex(-77, 32)

	assert list(Complex) == [Complex.a, Complex.b, Complex.c, Complex.d]

