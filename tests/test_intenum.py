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


def test_intenum_from_scratch():

	class phy(int, Enum):
		pi = 3
		tau = 2 * pi

	assert phy.pi < phy.tau


def test_intenum_inherited():

	class IntEnum(int, Enum):
		pass

	class phy(IntEnum):
		pi = 3
		tau = 2 * pi

	assert phy.pi < phy.tau



# These are unordered here on purpose to ensure that declaration order
# makes no difference.
CONVERT_TEST_NAME_D = 5
CONVERT_TEST_NAME_C = 5
CONVERT_TEST_NAME_B = 5
CONVERT_TEST_NAME_A = 5  # This one should sort first.
CONVERT_TEST_NAME_E = 5
CONVERT_TEST_NAME_F = 5
CONVERT_TEST_SIGABRT = 4  # and this one
CONVERT_TEST_SIGIOT = 4
CONVERT_TEST_EIO = 7
CONVERT_TEST_EBUS = 7  # and this one


class TestIntEnumConvert(TestCase):

	def test_convert_value_lookup_priority(self):
		test_type = IntEnum._convert('UnittestConvert', __name__, filter=lambda x: x.startswith('CONVERT_TEST_'))
		# We don't want the reverse lookup value to vary when there are
		# multiple possible names for a given value.  It should always
		# report the first lexigraphical name in that case.
		assert test_type(5).name == 'CONVERT_TEST_NAME_A'
		assert test_type(4).name == 'CONVERT_TEST_SIGABRT'
		assert test_type(7).name == 'CONVERT_TEST_EBUS'
		assert list(test_type) == [
				test_type.CONVERT_TEST_SIGABRT,
				test_type.CONVERT_TEST_NAME_A,
				test_type.CONVERT_TEST_EBUS,
				]

	def test_convert(self):
		test_type = IntEnum._convert('UnittestConvert', __name__, filter=lambda x: x.startswith('CONVERT_TEST_'))
		# Ensure that test_type has all of the desired names and values.
		assert test_type.CONVERT_TEST_NAME_F == test_type.CONVERT_TEST_NAME_A
		assert test_type.CONVERT_TEST_NAME_B == 5
		assert test_type.CONVERT_TEST_NAME_C == 5
		assert test_type.CONVERT_TEST_NAME_D == 5
		assert test_type.CONVERT_TEST_NAME_E == 5
		# Ensure that test_type only picked up names matching the filter.
		self.assertEqual(
				[name for name in dir(test_type) if name[0:2] not in ('CO', '__')],
				[],
				msg='Names other than CONVERT_TEST_* found.',
				)
