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
import sys

# this package
from better_enum import Enum, IntEnum, unique

pyver = float('%s.%s' % sys.version_info[:2])


def test_unique_clean():

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


def test_unique_dirty():
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
	assert 'tres -> one' in message

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
	assert 'double -> single' in message
	assert 'turkey -> triple' in message


def test_unique_with_name():

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
