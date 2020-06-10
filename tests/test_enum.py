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
import os
from collections import OrderedDict
from datetime import timedelta
from enum import Enum as StdlibEnum
from enum import EnumMeta as StdlibEnumMeta
from unittest import TestCase

# 3rd party
from aenum import EnumMeta, _decompose, _high_bit, auto, enum, extend_enum, skip  # type: ignore
from tests.conftest import tempdir
from tests.demo_classes import IntStooges, Name

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


class TestEnum(TestCase):

	def setUp(self):

		class Season(Enum):
			SPRING = 1
			SUMMER = 2
			AUTUMN = 3
			WINTER = 4

		self.Season = Season

		class Konstants(float, Enum):
			E = 2.7182818
			PI = 3.1415926
			TAU = 2 * PI

		self.Konstants = Konstants

		class Grades(IntEnum):
			A = 5
			B = 4
			C = 3
			D = 2
			F = 0

		self.Grades = Grades

		class Directional(str, Enum):
			EAST = 'east'
			WEST = 'west'
			NORTH = 'north'
			SOUTH = 'south'

		self.Directional = Directional

		from datetime import date

		class Holiday(date, Enum):
			NEW_YEAR = 2013, 1, 1
			IDES_OF_MARCH = 2013, 3, 15

		self.Holiday = Holiday

	def test_members_is_ordereddict_if_ordered(self):

		class Ordered(Enum):
			__order__ = 'first second third'
			first = 'bippity'
			second = 'boppity'
			third = 'boo'

		assert isinstance(Ordered.__members__, OrderedDict)

	def test_members_is_ordereddict_if_not_ordered(self):

		class Unordered(Enum):
			this = 'that'
			these = 'those'

		assert isinstance(Unordered.__members__, OrderedDict)

	def test_enum_in_enum_out(self):
		season = self.Season
		assert season(season.WINTER) is season.WINTER

	def test_enum_value(self):
		season = self.Season
		assert season.SPRING.value == 1

	def test_intenum_value(self):
		assert IntStooges.CURLY.value == 2

	def test_enum(self):
		lst = list(self.Season)
		assert len(lst) == len(self.Season)
		self.assertEqual(len(self.Season), 4, self.Season)
		assert [self.Season.SPRING, self.Season.SUMMER, self.Season.AUTUMN, self.Season.WINTER] == lst

		for i, season in enumerate('SPRING SUMMER AUTUMN WINTER'.split()):
			i += 1
			e = self.Season(i)
			assert e, getattr(self.Season == season)
			assert e.value == i
			assert e != i
			assert e.name == season
			assert e in self.Season
			assert isinstance(e, self.Season)
			assert isinstance(e, self.Season)
			assert str(e) == 'Season.' + season
			assert repr(e) == '<Season.%s: %s>' % (season, i)

	def test_enum_helper(self):
		e1 = enum(1, 2, three=9)
		e2 = enum(1, 2, three=9)
		e3 = enum(1, 2, 9)
		assert e1 is not e2
		assert e1 == e2
		assert e1 != e3
		assert e2 != e3

	def test_value_name(self):
		assert self.Season.SPRING.name == 'SPRING'
		assert self.Season.SPRING.value == 1

		def set_name(obj, new_value):
			obj.name = new_value

		def set_value(obj, new_value):
			obj.value = new_value

		self.assertRaises(
				AttributeError,
				set_name,
				self.Season.SPRING,
				'invierno',
				)
		self.assertRaises(AttributeError, set_value, self.Season.SPRING, 2)

	def test_attribute_deletion(self):

		class Season(Enum):
			SPRING = 1
			SUMMER = 2
			AUTUMN = 3
			WINTER = 4

			def spam(cls):
				pass

		assert hasattr(Season, 'spam')
		del Season.spam
		assert not hasattr(Season, 'spam')

		self.assertRaises(AttributeError, delattr, Season, 'SPRING')
		self.assertRaises(AttributeError, delattr, Season, 'DRY')
		self.assertRaises(AttributeError, delattr, Season.SPRING, 'name')

	def test_bool_of_class(self):

		class Empty(Enum):
			pass

		assert bool(Empty)

	def test_bool_of_member(self):

		class Count(Enum):
			zero = 0
			one = 1
			two = 2

		for member in Count:
			assert bool(member)

	def test_invalid_names(self):

		def create_bad_class_1():

			class Wrong(Enum):
				mro = 9

		def create_bad_class_2():

			class Wrong(Enum):
				_reserved_ = 3

		self.assertRaises(ValueError, create_bad_class_1)
		self.assertRaises(ValueError, create_bad_class_2)

	def test_bool(self):

		class Logic(Enum):
			true = True
			false = False

			def __bool__(self):
				return bool(self.value)

			__nonzero__ = __bool__

		assert Logic.true
		assert not Logic.false

	def test_contains(self):
		Season = self.Season
		self.assertRaises(TypeError, lambda: 'AUTUMN' in Season)
		assert Season.AUTUMN in Season
		self.assertRaises(TypeError, lambda: 3 not in Season)
		val = Season(3)
		assert val in Season

		#
		class OtherEnum(Enum):
			one = 1
			two = 2

		assert OtherEnum.two not in Season

		#
		class Wierd(Enum):
			this = [1, 2, 3]
			that = (1, 2, 3)
			those = {1: 1, 2: 2, 3: 3}

		assert Wierd.this in Wierd
		self.assertRaises(TypeError, lambda: [1, 2, 3] in Wierd)
		self.assertRaises(TypeError, lambda: {1: 1, 2: 2, 3: 3} in Wierd)

	def test_member_contains(self):
		self.assertRaises(TypeError, lambda: 'test' in self.Season.AUTUMN)

	def test_format_enum(self):
		Season = self.Season
		assert '{0}'.format(Season.SPRING) == '{0}'.format(str(Season.SPRING))
		assert '{0:}'.format(Season.SPRING) == '{0:}'.format(str(Season.SPRING))
		assert '{0:20}'.format(Season.SPRING) == '{0:20}'.format(str(Season.SPRING))
		assert '{0:^20}'.format(Season.SPRING) == '{0:^20}'.format(str(Season.SPRING))
		assert '{0:>20}'.format(Season.SPRING) == '{0:>20}'.format(str(Season.SPRING))
		assert '{0:<20}'.format(Season.SPRING) == '{0:<20}'.format(str(Season.SPRING))

	def test_format_enum_custom(self):

		class TestFloat(float, Enum):
			one = 1.0
			two = 2.0

			def __format__(self, spec):
				return 'TestFloat success!'

		assert '{0}'.format(TestFloat.one) == 'TestFloat success!'

	def assertFormatIsValue(self, spec, member):
		assert spec.format(member) == spec.format(member.value)

	def test_format_enum_date(self):
		Holiday = self.Holiday
		self.assertFormatIsValue('{0}', Holiday.IDES_OF_MARCH)
		self.assertFormatIsValue('{0:}', Holiday.IDES_OF_MARCH)
		self.assertFormatIsValue('{0:20}', Holiday.IDES_OF_MARCH)
		self.assertFormatIsValue('{0:^20}', Holiday.IDES_OF_MARCH)
		self.assertFormatIsValue('{0:>20}', Holiday.IDES_OF_MARCH)
		self.assertFormatIsValue('{0:<20}', Holiday.IDES_OF_MARCH)
		self.assertFormatIsValue('{0:%Y %m}', Holiday.IDES_OF_MARCH)
		self.assertFormatIsValue('{0:%Y %m %M:00}', Holiday.IDES_OF_MARCH)

	def test_format_enum_float(self):
		Konstants = self.Konstants
		self.assertFormatIsValue('{0}', Konstants.TAU)
		self.assertFormatIsValue('{0:}', Konstants.TAU)
		self.assertFormatIsValue('{0:20}', Konstants.TAU)
		self.assertFormatIsValue('{0:^20}', Konstants.TAU)
		self.assertFormatIsValue('{0:>20}', Konstants.TAU)
		self.assertFormatIsValue('{0:<20}', Konstants.TAU)
		self.assertFormatIsValue('{0:n}', Konstants.TAU)
		self.assertFormatIsValue('{0:5.2}', Konstants.TAU)
		self.assertFormatIsValue('{0:f}', Konstants.TAU)

	def test_format_enum_int(self):
		Grades = self.Grades
		self.assertFormatIsValue('{0}', Grades.C)
		self.assertFormatIsValue('{0:}', Grades.C)
		self.assertFormatIsValue('{0:20}', Grades.C)
		self.assertFormatIsValue('{0:^20}', Grades.C)
		self.assertFormatIsValue('{0:>20}', Grades.C)
		self.assertFormatIsValue('{0:<20}', Grades.C)
		self.assertFormatIsValue('{0:+}', Grades.C)
		self.assertFormatIsValue('{0:08X}', Grades.C)
		self.assertFormatIsValue('{0:b}', Grades.C)

	def test_format_enum_str(self):
		Directional = self.Directional
		self.assertFormatIsValue('{0}', Directional.WEST)
		self.assertFormatIsValue('{0:}', Directional.WEST)
		self.assertFormatIsValue('{0:20}', Directional.WEST)
		self.assertFormatIsValue('{0:^20}', Directional.WEST)
		self.assertFormatIsValue('{0:>20}', Directional.WEST)
		self.assertFormatIsValue('{0:<20}', Directional.WEST)

	def test_hash(self):
		Season = self.Season
		dates = {}
		dates[Season.WINTER] = '1225'
		dates[Season.SPRING] = '0315'
		dates[Season.SUMMER] = '0704'
		dates[Season.AUTUMN] = '1031'
		assert dates[Season.AUTUMN] == '1031'

	def test_enum_duplicates(self):

		class Season(Enum):
			__order__ = "SPRING SUMMER AUTUMN WINTER"
			SPRING = 1
			SUMMER = 2
			AUTUMN = FALL = 3
			WINTER = 4
			ANOTHER_SPRING = 1

		lst = list(Season)
		self.assertEqual(lst, [
				Season.SPRING,
				Season.SUMMER,
				Season.AUTUMN,
				Season.WINTER,
				])
		assert Season.FALL is Season.AUTUMN
		assert Season.FALL.value == 3
		assert Season.AUTUMN.value == 3
		assert Season(3) is Season.AUTUMN
		assert Season(1) is Season.SPRING
		assert Season.FALL.name == 'AUTUMN'
		assert set([k for k, v in Season.__members__.items() if v.name != k]) == set(['FALL', 'ANOTHER_SPRING'])

	def test_enum_with_value_name(self):

		class Huh(Enum):
			_order_ = 'name value'
			name = 1
			value = 2

		assert list(Huh) == [Huh.name, Huh.value]
		assert isinstance(Huh.name, Huh)
		assert Huh.name.name == 'name'
		assert Huh.name.value == 1

	def test_intenum_from_scratch(self):

		class phy(int, Enum):
			pi = 3
			tau = 2 * pi

		assert phy.pi < phy.tau

	def test_intenum_inherited(self):

		class IntEnum(int, Enum):
			pass

		class phy(IntEnum):
			pi = 3
			tau = 2 * pi

		assert phy.pi < phy.tau

	def test_floatenum_from_scratch(self):

		class phy(float, Enum):
			pi = 3.1415926
			tau = 2 * pi

		assert phy.pi < phy.tau

	def test_floatenum_inherited(self):

		class FloatEnum(float, Enum):
			pass

		class phy(FloatEnum):
			pi = 3.1415926
			tau = 2 * pi

		assert phy.pi < phy.tau

	def test_strenum_from_scratch(self):

		class phy(str, Enum):
			pi = 'Pi'
			tau = 'Tau'

		assert phy.pi < phy.tau

	def test_strenum_inherited(self):

		class StrEnum(str, Enum):
			pass

		class phy(StrEnum):
			pi = 'Pi'
			tau = 'Tau'

		assert phy.pi < phy.tau

	def test_intenum(self):

		class WeekDay(IntEnum):
			SUNDAY = 1
			MONDAY = 2
			TUESDAY = 3
			WEDNESDAY = 4
			THURSDAY = 5
			FRIDAY = 6
			SATURDAY = 7

		assert ['a', 'b', 'c'][WeekDay.MONDAY] == 'c'
		assert [i for i in range(WeekDay.TUESDAY)], [0, 1 == 2]

		lst = list(WeekDay)
		assert len(lst) == len(WeekDay)
		assert len(WeekDay) == 7
		target = 'SUNDAY MONDAY TUESDAY WEDNESDAY THURSDAY FRIDAY SATURDAY'
		target = target.split()
		for i, weekday in enumerate(target):
			i += 1
			e = WeekDay(i)
			assert e == i
			assert int(e) == i
			assert e.name == weekday
			assert e in WeekDay
			assert lst.index(e) + 1 == i
			assert 0 < e < 8
			assert isinstance(e, WeekDay)
			assert isinstance(e, int)
			assert isinstance(e, Enum)

	def test_intenum_duplicates(self):

		class WeekDay(IntEnum):
			__order__ = 'SUNDAY MONDAY TUESDAY WEDNESDAY THURSDAY FRIDAY SATURDAY'
			SUNDAY = 1
			MONDAY = 2
			TUESDAY = TEUSDAY = 3
			WEDNESDAY = 4
			THURSDAY = 5
			FRIDAY = 6
			SATURDAY = 7

		assert WeekDay.TEUSDAY is WeekDay.TUESDAY
		assert WeekDay(3).name == 'TUESDAY'
		self.assertEqual([k for k, v in WeekDay.__members__.items() if v.name != k], [
				'TEUSDAY',
				])

	def test_string_enum(self):

		class SkillLevel(str, Enum):
			master = 'what is the sound of one hand clapping?'
			journeyman = 'why did the chicken cross the road?'
			apprentice = 'knock, knock!'

		assert SkillLevel.apprentice, 'knock == knock!'

	def test_getattr_getitem(self):

		class Period(Enum):
			morning = 1
			noon = 2
			evening = 3
			night = 4

		assert Period(2) is Period.noon
		assert getattr(Period, 'night') is Period.night
		assert Period['morning'] is Period.morning

	def test_getattr_dunder(self):
		Season = self.Season
		assert getattr(Season, '__hash__')

	def test_iteration_order(self):

		class Season(Enum):
			__order__ = 'SUMMER WINTER AUTUMN SPRING'
			SUMMER = 2
			WINTER = 4
			AUTUMN = 3
			SPRING = 1

		self.assertEqual(
				list(Season),
				[Season.SUMMER, Season.WINTER, Season.AUTUMN, Season.SPRING],
				)

	def test_iteration_order_reversed(self):
		self.assertEqual(
				list(reversed(self.Season)),
				[self.Season.WINTER, self.Season.AUTUMN, self.Season.SUMMER, self.Season.SPRING]
				)

	def test_iteration_order_with_unorderable_values(self):

		class Complex(Enum):
			a = complex(7, 9)
			b = complex(3.14, 2)
			c = complex(1, -1)
			d = complex(-77, 32)

		self.assertEqual(
				list(Complex),
				[Complex.a, Complex.b, Complex.c, Complex.d],
				)

	def test_programatic_function_string(self):
		SummerMonth = Enum('SummerMonth', 'june july august')
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)
		self.assertEqual(
				[SummerMonth.june, SummerMonth.july, SummerMonth.august],
				lst,
				)
		for i, month in enumerate('june july august'.split()):
			i += 1
			e = SummerMonth(i)
			assert int(e.value) == i
			assert e != i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_string_with_start(self):
		SummerMonth = Enum('SummerMonth', 'june july august', start=10)
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)
		self.assertEqual(
				[SummerMonth.june, SummerMonth.july, SummerMonth.august],
				lst,
				)
		for i, month in enumerate('june july august'.split(), 10):
			e = SummerMonth(i)
			assert int(e.value) == i
			assert e != i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_string_list(self):
		SummerMonth = Enum('SummerMonth', ['june', 'july', 'august'])
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)
		self.assertEqual(
				[SummerMonth.june, SummerMonth.july, SummerMonth.august],
				lst,
				)
		for i, month in enumerate('june july august'.split()):
			i += 1
			e = SummerMonth(i)
			assert int(e.value) == i
			assert e != i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_string_list_with_start(self):
		SummerMonth = Enum('SummerMonth', ['june', 'july', 'august'], start=20)
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)
		self.assertEqual(
				[SummerMonth.june, SummerMonth.july, SummerMonth.august],
				lst,
				)
		for i, month in enumerate('june july august'.split(), 20):
			e = SummerMonth(i)
			assert int(e.value) == i
			assert e != i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_iterable(self):
		SummerMonth = Enum('SummerMonth', (('june', 1), ('july', 2), ('august', 3)))
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)
		self.assertEqual(
				[SummerMonth.june, SummerMonth.july, SummerMonth.august],
				lst,
				)
		for i, month in enumerate('june july august'.split()):
			i += 1
			e = SummerMonth(i)
			assert int(e.value) == i
			assert e != i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_from_dict(self):
		SummerMonth = Enum('SummerMonth', dict((('june', 1), ('july', 2), ('august', 3))))
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)

		for i, month in enumerate('june july august'.split()):
			i += 1
			e = SummerMonth(i)
			assert int(e.value) == i
			assert e != i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_type(self):
		SummerMonth = Enum('SummerMonth', 'june july august', type=int)
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)
		self.assertEqual(
				[SummerMonth.june, SummerMonth.july, SummerMonth.august],
				lst,
				)
		for i, month in enumerate('june july august'.split()):
			i += 1
			e = SummerMonth(i)
			assert e == i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_type_with_start(self):
		SummerMonth = Enum('SummerMonth', 'june july august', type=int, start=30)
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)
		self.assertEqual(
				[SummerMonth.june, SummerMonth.july, SummerMonth.august],
				lst,
				)
		for i, month in enumerate('june july august'.split(), 30):
			e = SummerMonth(i)
			assert e == i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_type_from_subclass(self):
		SummerMonth = IntEnum('SummerMonth', 'june july august')
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)
		self.assertEqual(
				[SummerMonth.june, SummerMonth.july, SummerMonth.august],
				lst,
				)
		for i, month in enumerate('june july august'.split()):
			i += 1
			e = SummerMonth(i)
			assert e == i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_type_from_subclass_with_start(self):
		SummerMonth = IntEnum('SummerMonth', 'june july august', start=40)
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)
		self.assertEqual(
				[SummerMonth.june, SummerMonth.july, SummerMonth.august],
				lst,
				)
		for i, month in enumerate('june july august'.split(), 40):
			e = SummerMonth(i)
			assert e == i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_unicode(self):
		SummerMonth = Enum('SummerMonth', str('june july august'))
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)
		self.assertEqual(
				[SummerMonth.june, SummerMonth.july, SummerMonth.august],
				lst,
				)
		for i, month in enumerate(str('june july august').split()):
			i += 1
			e = SummerMonth(i)
			assert int(e.value) == i
			assert e != i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_unicode_list(self):
		SummerMonth = Enum('SummerMonth', [str('june'), str('july'), str('august')])
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)
		self.assertEqual(
				[SummerMonth.june, SummerMonth.july, SummerMonth.august],
				lst,
				)
		for i, month in enumerate(str('june july august').split()):
			i += 1
			e = SummerMonth(i)
			assert int(e.value) == i
			assert e != i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_unicode_iterable(self):
		SummerMonth = Enum('SummerMonth', ((str('june'), 1), (str('july'), 2), (str('august'), 3)))
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)
		self.assertEqual(
				[SummerMonth.june, SummerMonth.july, SummerMonth.august],
				lst,
				)
		for i, month in enumerate(str('june july august').split()):
			i += 1
			e = SummerMonth(i)
			assert int(e.value) == i
			assert e != i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_from_unicode_dict(self):
		SummerMonth = Enum('SummerMonth', dict(((str('june'), 1), (str('july'), 2), (str('august'), 3))))
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)

		for i, month in enumerate(str('june july august').split()):
			i += 1
			e = SummerMonth(i)
			assert int(e.value) == i
			assert e != i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_unicode_type(self):
		SummerMonth = Enum('SummerMonth', str('june july august'), type=int)
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)
		self.assertEqual(
				[SummerMonth.june, SummerMonth.july, SummerMonth.august],
				lst,
				)
		for i, month in enumerate(str('june july august').split()):
			i += 1
			e = SummerMonth(i)
			assert e == i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programatic_function_unicode_type_from_subclass(self):
		SummerMonth = IntEnum('SummerMonth', str('june july august'))
		lst = list(SummerMonth)
		assert len(lst) == len(SummerMonth)
		self.assertEqual(len(SummerMonth), 3, SummerMonth)
		self.assertEqual(
				[SummerMonth.june, SummerMonth.july, SummerMonth.august],
				lst,
				)
		for i, month in enumerate(str('june july august').split()):
			i += 1
			e = SummerMonth(i)
			assert e == i
			assert e.name == month
			assert e in SummerMonth
			assert isinstance(e, SummerMonth)

	def test_programmatic_function_unicode_class(self):

		class_names = 'SummerMonth', 'S\xfcmm\xe9rM\xf6nth'
		for i, class_name in enumerate(class_names):

			SummerMonth = Enum(class_name, str('june july august'))
			lst = list(SummerMonth)
			assert len(lst) == len(SummerMonth)
			self.assertEqual(len(SummerMonth), 3, SummerMonth)
			assert [SummerMonth.june, SummerMonth.july, SummerMonth.august] == lst
			for i, month in enumerate(str('june july august').split()):
				i += 1
				e = SummerMonth(i)
				assert e.value == i
				assert e.name == month
				assert e in SummerMonth
				assert isinstance(e, SummerMonth)

	def test_subclassing(self):
		if isinstance(Name, Exception):
			raise Name
		assert Name.BDFL == 'Guido van Rossum'
		assert Name.BDFL, Name('Guido van Rossum')
		assert Name.BDFL is getattr(Name, 'BDFL')

	def test_extending(self):

		def bad_extension():

			class Color(Enum):
				red = 1
				green = 2
				blue = 3

			class MoreColor(Color):
				cyan = 4
				magenta = 5
				yellow = 6

		self.assertRaises(TypeError, bad_extension)

	def test_exclude_methods(self):

		class whatever(Enum):
			this = 'that'
			these = 'those'

			def really(self):
				return 'no, not %s' % self.value

		assert not isinstance(whatever.really, whatever)
		assert whatever.this.really(), 'no == not that'

	def test_wrong_inheritance_order(self):

		def wrong_inherit():

			class Wrong(Enum, str):
				NotHere = 'error before this point'

		self.assertRaises(TypeError, wrong_inherit)

	def test_intenum_transitivity(self):

		class number(IntEnum):
			one = 1
			two = 2
			three = 3

		class numero(IntEnum):
			uno = 1
			dos = 2
			tres = 3

		assert number.one == numero.uno
		assert number.two == numero.dos
		assert number.three == numero.tres

	def test_introspection(self):

		class Number(IntEnum):
			one = 100
			two = 200

		assert Number.one._member_type_ is int
		assert Number._member_type_ is int

		class String(str, Enum):
			yarn = 'soft'
			rope = 'rough'
			wire = 'hard'

		assert String.yarn._member_type_ is str
		assert String._member_type_ is str

		class Plain(Enum):
			vanilla = 'white'
			one = 1

		assert Plain.vanilla._member_type_ is object
		assert Plain._member_type_ is object

	def test_wrong_enum_in_call(self):

		class Monochrome(Enum):
			black = 0
			white = 1

		class Gender(Enum):
			male = 0
			female = 1

		self.assertRaises(ValueError, Monochrome, Gender.male)

	def test_wrong_enum_in_mixed_call(self):

		class Monochrome(IntEnum):
			black = 0
			white = 1

		class Gender(Enum):
			male = 0
			female = 1

		self.assertRaises(ValueError, Monochrome, Gender.male)

	def test_mixed_enum_in_call_1(self):

		class Monochrome(IntEnum):
			black = 0
			white = 1

		class Gender(IntEnum):
			male = 0
			female = 1

		assert Monochrome(Gender.female) is Monochrome.white

	def test_mixed_enum_in_call_2(self):

		class Monochrome(Enum):
			black = 0
			white = 1

		class Gender(IntEnum):
			male = 0
			female = 1

		assert Monochrome(Gender.male) is Monochrome.black

	def test_flufl_enum(self):

		class Fluflnum(Enum):

			def __int__(self):
				return int(self.value)

		class MailManOptions(Fluflnum):
			option1 = 1
			option2 = 2
			option3 = 3

		assert int(MailManOptions.option1) == 1

	def test_no_such_enum_member(self):

		class Color(Enum):
			red = 1
			green = 2
			blue = 3

		self.assertRaises(ValueError, Color, 4)
		self.assertRaises(KeyError, Color.__getitem__, 'chartreuse')

	def test_new_repr(self):

		class Color(Enum):
			red = 1
			green = 2
			blue = 3

			def __repr__(self):
				return "don't you just love shades of %s?" % self.name

		self.assertEqual(
				repr(Color.blue),
				"don't you just love shades of blue?",
				)

	def test_inherited_repr(self):

		class MyEnum(Enum):

			def __repr__(self):
				return "My name is %s." % self.name

		class MyIntEnum(int, MyEnum):
			this = 1
			that = 2
			theother = 3

		assert repr(MyIntEnum.that) == "My name is that."

	def test_multiple_mixin_mro(self):

		class auto_enum(EnumMeta):

			def __new__(metacls, cls, bases, classdict):
				original_dict = classdict
				temp_dict = metacls.__prepare__(cls, bases, {})
				if hasattr(original_dict, '_member_names'):
					for k in original_dict._member_names:
						temp_dict[k] = original_dict[k]
					sunders = [k for k in original_dict.keys() if _is_sunder(k)]
				else:
					sunders = []
					for k, v in original_dict.items():
						if _is_sunder(k):
							sunders.append(k)
						temp_dict[k] = v
				classdict = metacls.__prepare__(cls, bases, {})
				i = 0
				for k in sunders:
					classdict[k] = original_dict[k]
				for k in temp_dict._member_names:
					v = original_dict[k]
					if v == ():
						v = i
					else:
						i = v
					i += 1
					classdict[k] = v
				for k, v in original_dict.items():
					if k not in temp_dict._member_names and k not in sunders:
						classdict[k] = v
				return super(auto_enum, metacls).__new__(metacls, cls, bases, classdict)

		AutoNumberedEnum = auto_enum('AutoNumberedEnum', (Enum, ), {})

		AutoIntEnum = auto_enum('AutoIntEnum', (IntEnum, ), {})

		class TestAutoNumber(AutoNumberedEnum):
			a = ()
			b = 3
			c = ()

		assert TestAutoNumber.b.value == 3

		self.assertEqual(
				[TestAutoNumber.a.value, TestAutoNumber.b.value, TestAutoNumber.c.value],
				[0, 3, 4],
				)

		class TestAutoInt(AutoIntEnum):
			a = ()
			b = 3
			c = ()

		assert TestAutoInt.b == 3

		self.assertEqual(
				[TestAutoInt.a.value, TestAutoInt.b.value, TestAutoInt.c.value],
				[0, 3, 4],
				)

	def test_meta_reconfigure(self):

		def identity(*args):
			if len(args) == 1:
				return args[0]
			return args

		JSONEnum = None

		class JSONEnumMeta(EnumMeta):

			@classmethod
			def __prepare__(metacls, cls, bases, init=None, start=None, settings=()):
				return {}

			def __init__(cls, *args, **kwds):
				super(JSONEnumMeta, cls).__init__(*args)

			def __new__(metacls, cls, bases, clsdict, init=None, start=None, settings=()):
				import json
				members = []
				if JSONEnum is not None:
					if '_file' not in clsdict:
						raise TypeError('_file is required')
					if '_name' not in clsdict:
						raise TypeError('_name is required')
					if '_value' not in clsdict:
						raise TypeError('_value is required')
					name_spec = clsdict.pop('_name')
					if not isinstance(name_spec, (tuple, list)):
						name_spec = (name_spec, )
					value_spec = clsdict.pop('_value')
					file = clsdict.pop('_file')
					with open(file) as f:
						json_data = json.load(f)
					for data in json_data:
						values = []
						name = data[name_spec[0]]
						for piece in name_spec[1:]:
							name = name[piece]
						for order, (value_path, func) in sorted(value_spec.items()):
							if not isinstance(value_path, (list, tuple)):
								value_path = (value_path, )
							value = data[value_path[0]]
							for piece in value_path[1:]:
								value = value[piece]
							if func is not None:
								value = func(value)
							values.append(value)
						values = tuple(values)
						members.append((name, identity(*values)))
				# get the real EnumDict
				enum_dict = super(JSONEnumMeta, metacls).__prepare__(cls, bases, init, start, settings)
				# transfer the original dict content, _items first
				items = list(clsdict.items())
				items.sort(key=lambda p: (0 if p[0][0] == '_' else 1, p))
				for name, value in items:
					enum_dict[name] = value
				# add the members
				for name, value in members:
					enum_dict[name] = value
				return super(JSONEnumMeta, metacls).__new__(metacls, cls, bases, enum_dict, init, start, settings)

		# for use with both Python 2/3
		JSONEnum = JSONEnumMeta('JsonEnum', (Enum, ), {})

		test_file = os.path.join(tempdir, 'test_json.json')
		with open(test_file, 'w') as f:
			f.write(
					'[{"name":"Afghanistan","alpha-2":"AF","country-code":"004","notes":{"description":"pretty"}},'
					'{"name":"Åland Islands","alpha-2":"AX","country-code":"248","notes":{"description":"serene"}},'
					'{"name":"Albania","alpha-2":"AL","country-code":"008","notes":{"description":"exciting"}},'
					'{"name":"Algeria","alpha-2":"DZ","country-code":"012","notes":{"description":"scarce"}}]'
					)

		class Country(JSONEnum):
			_init_ = 'abbr code country_name description'
			_file = test_file
			_name = 'alpha-2'
			_value = {
					1: ('alpha-2', None),
					2: ('country-code', lambda c: int(c)),
					3: ('name', None),
					4: (('notes', 'description'), lambda s: s.title()),
					}

		assert [Country.AF, Country.AX, Country.AL, Country.DZ] == list(Country)
		assert Country.AF.abbr == 'AF'
		assert Country.AX.code == 248
		assert Country.AL.country_name == 'Albania'
		assert Country.DZ.description == 'Scarce'

	def test_subclasses_with_getnewargs(self):

		class NamedInt(int):
			__qualname__ = 'NamedInt'  # needed for pickle protocol 4

			def __new__(cls, *args):
				_args = args
				if len(args) < 1:
					raise TypeError("name and value must be specified")
				name, args = args[0], args[1:]
				self = int.__new__(cls, *args)
				self._intname = name
				self._args = _args
				return self

			def __getnewargs__(self):
				return self._args

			@property
			def __name__(self):
				return self._intname

			def __repr__(self):
				# repr() is updated to include the name and type info
				return "%s(%r, %s)" % (type(self).__name__, self.__name__, int.__repr__(self))

			def __str__(self):
				# str() is unchanged, even if it relies on the repr() fallback
				base = int
				base_str = base.__str__
				if base_str.__objclass__ is object:
					return base.__repr__(self)
				return base_str(self)

			# for simplicity, we only define one operator that
			# propagates expressions
			def __add__(self, other):
				temp = int(self) + int(other)
				if isinstance(self, NamedInt) and isinstance(other, NamedInt):
					return NamedInt('(%s + %s)' % (self.__name__, other.__name__), temp)
				else:
					return temp

		class NEI(NamedInt, Enum):
			__qualname__ = 'NEI'  # needed for pickle protocol 4
			x = ('the-x', 1)
			y = ('the-y', 2)

		assert NEI.__new__ is Enum.__new__
		assert repr(NEI.x + NEI.y), "NamedInt('(the-x + the-y)' == 3)"
		globals()['NamedInt'] = NamedInt
		globals()['NEI'] = NEI
		NI5 = NamedInt('test', 5)
		assert NI5 == 5
		assert NEI.y.value == 2

	def test_subclasses_with_reduce(self):

		class NamedInt(int):
			__qualname__ = 'NamedInt'  # needed for pickle protocol 4

			def __new__(cls, *args):
				_args = args
				if len(args) < 1:
					raise TypeError("name and value must be specified")
				name, args = args[0], args[1:]
				self = int.__new__(cls, *args)
				self._intname = name
				self._args = _args
				return self

			def __reduce__(self):
				return self.__class__, self._args

			@property
			def __name__(self):
				return self._intname

			def __repr__(self):
				# repr() is updated to include the name and type info
				return "%s(%r, %s)" % (type(self).__name__, self.__name__, int.__repr__(self))

			def __str__(self):
				# str() is unchanged, even if it relies on the repr() fallback
				base = int
				base_str = base.__str__
				if base_str.__objclass__ is object:
					return base.__repr__(self)
				return base_str(self)

			# for simplicity, we only define one operator that
			# propagates expressions
			def __add__(self, other):
				temp = int(self) + int(other)
				if isinstance(self, NamedInt) and isinstance(other, NamedInt):
					return NamedInt('(%s + %s)' % (self.__name__, other.__name__), temp)
				else:
					return temp

		class NEI(NamedInt, Enum):
			__qualname__ = 'NEI'  # needed for pickle protocol 4
			x = ('the-x', 1)
			y = ('the-y', 2)

		assert NEI.__new__ is Enum.__new__
		assert repr(NEI.x + NEI.y), "NamedInt('(the-x + the-y)' == 3)"
		globals()['NamedInt'] = NamedInt
		globals()['NEI'] = NEI
		NI5 = NamedInt('test', 5)
		assert NI5 == 5
		assert NEI.y.value == 2

	def test_subclasses_with_reduce_ex(self):

		class NamedInt(int):
			__qualname__ = 'NamedInt'  # needed for pickle protocol 4

			def __new__(cls, *args):
				_args = args
				if len(args) < 1:
					raise TypeError("name and value must be specified")
				name, args = args[0], args[1:]
				self = int.__new__(cls, *args)
				self._intname = name
				self._args = _args
				return self

			def __reduce_ex__(self, proto):
				return self.__class__, self._args

			@property
			def __name__(self):
				return self._intname

			def __repr__(self):
				# repr() is updated to include the name and type info
				return "%s(%r, %s)" % (type(self).__name__, self.__name__, int.__repr__(self))

			def __str__(self):
				# str() is unchanged, even if it relies on the repr() fallback
				base = int
				base_str = base.__str__
				if base_str.__objclass__ is object:
					return base.__repr__(self)
				return base_str(self)

			# for simplicity, we only define one operator that
			# propagates expressions
			def __add__(self, other):
				temp = int(self) + int(other)
				if isinstance(self, NamedInt) and isinstance(other, NamedInt):
					return NamedInt('(%s + %s)' % (self.__name__, other.__name__), temp)
				else:
					return temp

		class NEI(NamedInt, Enum):
			__qualname__ = 'NEI'  # needed for pickle protocol 4
			x = ('the-x', 1)
			y = ('the-y', 2)

		assert NEI.__new__ is Enum.__new__
		assert repr(NEI.x + NEI.y), "NamedInt('(the-x + the-y)' == 3)"
		globals()['NamedInt'] = NamedInt
		globals()['NEI'] = NEI
		NI5 = NamedInt('test', 5)
		assert NI5 == 5
		assert NEI.y.value == 2

	def test_subclasses_without_direct_pickle_support(self):

		class NamedInt(int):
			__qualname__ = 'NamedInt'

			def __new__(cls, *args):
				_args = args
				name, args = args[0], args[1:]
				if len(args) == 0:
					raise TypeError("name and value must be specified")
				self = int.__new__(cls, *args)
				self._intname = name
				self._args = _args
				return self

			@property
			def __name__(self):
				return self._intname

			def __repr__(self):
				# repr() is updated to include the name and type info
				return "%s(%r, %s)" % (type(self).__name__, self.__name__, int.__repr__(self))

			def __str__(self):
				# str() is unchanged, even if it relies on the repr() fallback
				base = int
				base_str = base.__str__
				if base_str.__objclass__ is object:
					return base.__repr__(self)
				return base_str(self)

			# for simplicity, we only define one operator that
			# propagates expressions
			def __add__(self, other):
				temp = int(self) + int(other)
				if isinstance(self, NamedInt) and isinstance(other, NamedInt):
					return NamedInt('(%s + %s)' % (self.__name__, other.__name__), temp)
				else:
					return temp

		class NEI(NamedInt, Enum):
			__qualname__ = 'NEI'
			x = ('the-x', 1)
			y = ('the-y', 2)

		assert NEI.__new__ is Enum.__new__
		assert repr(NEI.x + NEI.y), "NamedInt('(the-x + the-y)' == 3)"
		globals()['NamedInt'] = NamedInt
		globals()['NEI'] = NEI
		NI5 = NamedInt('test', 5)
		assert NI5 == 5
		assert NEI.y.value == 2

	def test_subclasses_without_direct_pickle_support_using_name(self):

		class NamedInt(int):
			__qualname__ = 'NamedInt'

			def __new__(cls, *args):
				_args = args
				name, args = args[0], args[1:]
				if len(args) == 0:
					raise TypeError("name and value must be specified")
				self = int.__new__(cls, *args)
				self._intname = name
				self._args = _args
				return self

			@property
			def __name__(self):
				return self._intname

			def __repr__(self):
				# repr() is updated to include the name and type info
				return "%s(%r, %s)" % (type(self).__name__, self.__name__, int.__repr__(self))

			def __str__(self):
				# str() is unchanged, even if it relies on the repr() fallback
				base = int
				base_str = base.__str__
				if base_str.__objclass__ is object:
					return base.__repr__(self)
				return base_str(self)

			# for simplicity, we only define one operator that
			# propagates expressions
			def __add__(self, other):
				temp = int(self) + int(other)
				if isinstance(self, NamedInt) and isinstance(other, NamedInt):
					return NamedInt('(%s + %s)' % (self.__name__, other.__name__), temp)
				else:
					return temp

		class NEI(NamedInt, Enum):
			__qualname__ = 'NEI'
			x = ('the-x', 1)
			y = ('the-y', 2)

			def __reduce_ex__(self, proto):
				return getattr, (self.__class__, self._name_)

		assert NEI.__new__ is Enum.__new__
		assert repr(NEI.x + NEI.y), "NamedInt('(the-x + the-y)' == 3)"
		globals()['NamedInt'] = NamedInt
		globals()['NEI'] = NEI
		NI5 = NamedInt('test', 5)
		assert NI5 == 5
		assert NEI.y.value == 2

	def test_tuple_subclass(self):

		class SomeTuple(tuple, Enum):
			__qualname__ = 'SomeTuple'
			first = (1, 'for the money')
			second = (2, 'for the show')
			third = (3, 'for the music')

		assert isinstance(SomeTuple.first, SomeTuple)
		assert isinstance(SomeTuple.second, tuple)
		assert SomeTuple.third, (3 == 'for the music')
		globals()['SomeTuple'] = SomeTuple

	def test_duplicate_values_give_unique_enum_items(self):

		class NumericEnum(AutoNumberEnum):
			__order__ = 'enum_m enum_d enum_y'
			enum_m = ()
			enum_d = ()
			enum_y = ()

			def __int__(self):
				return int(self._value_)

		assert int(NumericEnum.enum_d) == 2
		assert NumericEnum.enum_y.value == 3
		assert NumericEnum(1) is NumericEnum.enum_m
		self.assertEqual(
				list(NumericEnum),
				[NumericEnum.enum_m, NumericEnum.enum_d, NumericEnum.enum_y],
				)

	def test_inherited_new_from_enhanced_enum(self):

		class AutoNumber2(Enum):

			def __new__(cls):
				value = len(cls.__members__) + 1
				obj = object.__new__(cls)
				obj._value_ = value
				return obj

			def __int__(self):
				return int(self._value_)

		class Color(AutoNumber2):
			__order__ = 'red green blue'
			red = ()
			green = ()
			blue = ()

		self.assertEqual(len(Color), 3, "wrong number of elements: %d (should be %d)" % (len(Color), 3))
		self.assertEqual(list(Color), [Color.red, Color.green, Color.blue])

		assert list(map(int, Color)), [1, 2 == 3]

	def test_inherited_new_from_mixed_enum(self):

		class AutoNumber3(IntEnum):

			def __new__(cls):
				value = len(cls.__members__) + 11
				obj = int.__new__(cls, value)
				obj._value_ = value
				return obj

		class Color(AutoNumber3):
			__order__ = 'red green blue'
			red = ()
			green = ()
			blue = ()

		self.assertEqual(len(Color), 3, "wrong number of elements: %d (should be %d)" % (len(Color), 3))
		Color.red  # pylint: disable=pointless-statement
		Color.green  # pylint: disable=pointless-statement
		Color.blue  # pylint: disable=pointless-statement
		assert Color.blue == 13

	def test_equality(self):

		class AlwaysEqual:

			def __eq__(self, other):
				return True

		class OrdinaryEnum(Enum):
			a = 1

		assert AlwaysEqual() == OrdinaryEnum.a
		assert OrdinaryEnum.a == AlwaysEqual()

	def test_ordered_mixin(self):

		class Grade(OrderedEnum):
			__order__ = 'A B C D F'
			A = 5
			B = 4
			C = 3
			D = 2
			F = 1

		assert list(Grade), [Grade.A, Grade.B, Grade.C, Grade.D == Grade.F]
		assert Grade.A > Grade.B
		assert Grade.F <= Grade.C
		assert Grade.D < Grade.A
		assert Grade.B >= Grade.B

	def test_missing_deprecated(self):

		class Label(Enum):
			AnyApple = 0
			RedApple = 1
			GreenApple = 2

			@classmethod
			def _missing_(cls, name):
				return cls.AnyApple

		assert Label.AnyApple == Label(4)
		with self.assertRaises(AttributeError):
			Label.redapple  # pylint: disable=pointless-statement
		with self.assertRaises(KeyError):
			Label['redapple']  # pylint: disable=pointless-statement

	def test_missing(self):

		class Label(Enum):
			AnyApple = 0
			RedApple = 1
			GreenApple = 2

			@classmethod
			def _missing_value_(cls, name):
				return cls.AnyApple

		assert Label.AnyApple == Label(4)
		with self.assertRaises(AttributeError):
			Label.redapple  # pylint: disable=pointless-statement
		with self.assertRaises(KeyError):
			Label['redapple']  # pylint: disable=pointless-statement

	def test_missing_name(self):

		class Label(Enum):
			RedApple = 1
			GreenApple = 2

			@classmethod
			def _missing_name_(cls, name):
				for member in cls:
					if member.name.lower() == name.lower():
						return member

		Label['redapple']  # noqa  # pylint: disable=pointless-statement
		with self.assertRaises(AttributeError):
			Label.redapple  # noqa  # pylint: disable=pointless-statement
		with self.assertRaises(ValueError):
			Label('redapple')

	def test_missing_name_bad_return(self):

		class Label(Enum):
			RedApple = 1
			GreenApple = 2

			@classmethod
			def _missing_name_(cls, name):
				return None

		with self.assertRaises(AttributeError):
			Label.redapple  # noqa  # pylint: disable=pointless-statement
		with self.assertRaises(ValueError):
			Label('redapple')
		with self.assertRaises(KeyError):
			Label['redapple']  # noqa  # pylint: disable=pointless-statement

	def test_extending2(self):

		def bad_extension():

			class Shade(Enum):

				def shade(self):
					print(self.name)

			class Color(Shade):
				red = 1
				green = 2
				blue = 3

			class MoreColor(Color):
				cyan = 4
				magenta = 5
				yellow = 6

		self.assertRaises(TypeError, bad_extension)

	def test_extending3(self):

		class Shade(Enum):

			def shade(self):
				return self.name

		class Color(Shade):

			def hex(self):
				return f'{self.value} hexlified!'

		class MoreColor(Color):
			cyan = 4
			magenta = 5
			yellow = 6

		assert MoreColor.magenta.hex() == '5 hexlified!'

	def test_extend_enum_plain(self):

		class Color(UniqueEnum):
			red = 1
			green = 2
			blue = 3

		extend_enum(Color, 'brown', 4)
		assert Color.brown.name == 'brown'
		assert Color.brown.value == 4
		assert Color.brown in Color
		assert Color(4) == Color.brown
		assert Color['brown'] == Color.brown
		assert len(Color) == 4

	def test_extend_enum_alias(self):

		class Color(Enum):
			red = 1
			green = 2
			blue = 3

		extend_enum(Color, 'rojo', 1)
		assert Color.rojo.name == 'red'
		assert Color.rojo.value == 1
		assert Color.rojo in Color
		assert Color(1) == Color.rojo
		assert Color['rojo'] == Color.red
		assert len(Color) == 3

	def test_extend_enum_no_alias(self):

		class Color(UniqueEnum):
			red = 1
			green = 2
			blue = 3

		self.assertRaisesRegex(ValueError, 'rojo is a duplicate of red', extend_enum, Color, 'rojo', 1)
		assert Color.red.name == 'red'
		assert Color.red.value == 1
		assert Color.red in Color
		assert Color(1) == Color.red
		assert Color['red'] == Color.red
		assert Color.green.name == 'green'
		assert Color.green.value == 2
		assert Color.green in Color
		assert Color(2) == Color.green
		assert Color['blue'] == Color.blue
		assert Color.blue.name == 'blue'
		assert Color.blue.value == 3
		assert Color.blue in Color
		assert Color(3) == Color.blue
		assert len(Color) == 3

	def test_extend_enum_shadow(self):

		class Color(UniqueEnum):
			red = 1
			green = 2
			blue = 3

		extend_enum(Color, 'value', 4)
		assert Color.value.name == 'value'
		assert Color.value.value == 4
		assert Color.value in Color
		assert Color(4) == Color.value
		assert Color['value'] == Color.value
		assert len(Color) == 4
		assert Color.red.value == 1

	def test_extend_enum_multivalue(self):

		class Color(MultiValueEnum):
			red = 1, 4, 7
			green = 2, 5, 8
			blue = 3, 6, 9

		extend_enum(Color, 'brown', 10, 20)
		assert Color.brown.name == 'brown'
		assert Color.brown.value == 10
		assert Color.brown in Color
		assert Color(10) == Color.brown
		assert Color(20) == Color.brown
		assert Color['brown'] == Color.brown
		assert len(Color) == 4

	def test_extend_enum_multivalue_alias(self):

		class Color(MultiValueEnum):
			red = 1, 4, 7
			green = 2, 5, 8
			blue = 3, 6, 9

		self.assertRaisesRegex(ValueError, 'rojo is a duplicate of red', extend_enum, Color, 'rojo', 7)
		assert Color.red.name == 'red'
		assert Color.red.value == 1
		assert Color.red in Color
		assert Color(1) == Color.red
		assert Color(4) == Color.red
		assert Color(7) == Color.red
		assert Color['red'] == Color.red
		assert Color.green.name == 'green'
		assert Color.green.value == 2
		assert Color.green in Color
		assert Color(2) == Color.green
		assert Color(5) == Color.green
		assert Color(8) == Color.green
		assert Color['blue'] == Color.blue
		assert Color.blue.name == 'blue'
		assert Color.blue.value == 3
		assert Color.blue in Color
		assert Color(3) == Color.blue
		assert Color(6) == Color.blue
		assert Color(9) == Color.blue
		assert len(Color) == 3

	def test_extend_intenum(self):

		class Index(IntEnum):
			DeviceType = 0x1000
			ErrorRegister = 0x1001

		for name, value in (
			('ControlWord', 0x6040),
			('StatusWord', 0x6041),
			('OperationMode', 0x6060),
			):
			extend_enum(Index, name, value)

		assert len(Index) == 5
		self.assertEqual(
				list(Index),
				[Index.DeviceType, Index.ErrorRegister, Index.ControlWord, Index.StatusWord, Index.OperationMode]
				)
		assert Index.DeviceType.value == 0x1000
		assert Index.StatusWord.value == 0x6041

	def test_extend_multi_init(self):

		class HTTPStatus(IntEnum):

			def __new__(cls, value, phrase, description=''):
				obj = int.__new__(cls, value)
				obj._value_ = value

				obj.phrase = phrase
				obj.description = description
				return obj

			CONTINUE = 100, 'Continue', 'Request received, please continue'
			SWITCHING_PROTOCOLS = 101, 'Switching Protocols', 'Switching to new protocol; obey Upgrade header'
			PROCESSING = 102, 'Processing'

		extend_enum(HTTPStatus, 'BAD_SPAM', 513, 'Too greasy', 'for a train')
		extend_enum(HTTPStatus, 'BAD_EGGS', 514, 'Too green')
		assert len(HTTPStatus) == 5
		self.assertEqual(
				list(HTTPStatus),
				[
						HTTPStatus.CONTINUE,
						HTTPStatus.SWITCHING_PROTOCOLS,
						HTTPStatus.PROCESSING,
						HTTPStatus.BAD_SPAM,
						HTTPStatus.BAD_EGGS
						],
				)
		assert HTTPStatus.BAD_SPAM.value == 513
		assert HTTPStatus.BAD_SPAM.name == 'BAD_SPAM'
		assert HTTPStatus.BAD_SPAM.phrase == 'Too greasy'
		assert HTTPStatus.BAD_SPAM.description == 'for a train'
		assert HTTPStatus.BAD_EGGS.value == 514
		assert HTTPStatus.BAD_EGGS.name == 'BAD_EGGS'
		assert HTTPStatus.BAD_EGGS.phrase == 'Too green'
		assert HTTPStatus.BAD_EGGS.description == ''

	def test_no_duplicates(self):

		def bad_duplicates():

			class Color1(UniqueEnum):
				red = 1
				green = 2
				blue = 3

			class Color2(UniqueEnum):
				red = 1
				green = 2
				blue = 3
				grene = 2

		self.assertRaises(ValueError, bad_duplicates)

	def test_no_duplicates_kinda(self):

		class Silly(UniqueEnum):
			one = 1
			two = 'dos'
			name = 3

		class Sillier(IntEnum, UniqueEnum):
			single = 1
			name = 2
			triple = 3
			value = 4

	def test_init(self):

		class Planet(Enum):
			MERCURY = (3.303e+23, 2.4397e6)
			VENUS = (4.869e+24, 6.0518e6)
			EARTH = (5.976e+24, 6.37814e6)
			MARS = (6.421e+23, 3.3972e6)
			JUPITER = (1.9e+27, 7.1492e7)
			SATURN = (5.688e+26, 6.0268e7)
			URANUS = (8.686e+25, 2.5559e7)
			NEPTUNE = (1.024e+26, 2.4746e7)

			def __init__(self, mass, radius):
				self.mass = mass  # in kilograms
				self.radius = radius  # in meters

			@property
			def surface_gravity(self):
				# universal gravitational constant  (m3 kg-1 s-2)
				G = 6.67300E-11
				return G * self.mass / (self.radius * self.radius)

		assert round(Planet.EARTH.surface_gravity, 2) == 9.80
		assert Planet.EARTH.value, (5.976e+24 == 6.37814e6)

		@skip
		def test_init_and_autonumber(self):
			pass

		@skip
		def test_init_and_autonumber_and_value(self):
			pass

	def test_no_init_and_autonumber(self):

		class DocEnum(str, Enum):
			"""
			compares equal to all cased versions of its name
			accepts a docstring for each member
			"""
			_settings_ = AutoNumber

			def __init__(self, value, doc=None):
				# first, fix _value_
				self._value_ = self._name_.lower()
				self.__doc__ = doc

			def __eq__(self, other):
				if isinstance(other, str):
					return self._value_ == other.lower()
				elif isinstance(other, self.__class__):
					return self is other
				else:
					return False

			def __ne__(self, other):
				return not self == other

			REQUIRED = "required value"
			OPTION = "single value per name"
			MULTI = "multiple values per name (list form, no whitespace)"
			FLAG = "boolean/trivalent value per name"
			KEYWORD = 'unknown options'

		assert DocEnum.REQUIRED == 'required'
		assert DocEnum.REQUIRED == 'Required'
		assert DocEnum.REQUIRED == 'REQUIRED'

	def test_nonhash_value(self):

		class AutoNumberInAList(Enum):

			def __new__(cls):
				value = [len(cls.__members__) + 1]
				obj = object.__new__(cls)
				obj._value_ = value
				return obj

		class ColorInAList(AutoNumberInAList):
			__order__ = 'red green blue'
			red = ()
			green = ()
			blue = ()

		assert list(ColorInAList), [ColorInAList.red, ColorInAList.green == ColorInAList.blue]
		assert ColorInAList.red.value == [1]
		assert ColorInAList([1]) == ColorInAList.red

	def test_conflicting_types_resolved_in_new(self):

		class LabelledIntEnum(int, Enum):

			def __new__(cls, *args):
				value, label = args
				obj = int.__new__(cls, value)
				obj.label = label
				obj._value_ = value
				return obj

		class LabelledList(LabelledIntEnum):
			unprocessed = (1, "Unprocessed")
			payment_complete = (2, "Payment Complete")

		assert LabelledList.unprocessed == 1
		assert LabelledList(1) == LabelledList.unprocessed
		assert list(LabelledList), [LabelledList.unprocessed == LabelledList.payment_complete]

	def test_auto_number(self):

		class Color(Enum):
			_order_ = 'red blue green'
			red = auto()
			blue = auto()
			green = auto()

		assert list(Color), [Color.red, Color.blue == Color.green]
		assert Color.red.value == 1
		assert Color.blue.value == 2
		assert Color.green.value == 3

	def test_auto_name(self):

		class Color(Enum):
			_order_ = 'red blue green'

			def _generate_next_value_(name, start, count, last):
				return name

			red = auto()
			blue = auto()
			green = auto()

		assert list(Color), [Color.red, Color.blue == Color.green]
		assert Color.red.value == 'red'
		assert Color.blue.value == 'blue'
		assert Color.green.value == 'green'

	def test_auto_name_inherit(self):

		class AutoNameEnum(Enum):

			def _generate_next_value_(name, start, count, last):
				return name

		class Color(AutoNameEnum):
			_order_ = 'red blue green'
			red = auto()
			blue = auto()
			green = auto()

		assert list(Color), [Color.red, Color.blue == Color.green]
		assert Color.red.value == 'red'
		assert Color.blue.value == 'blue'
		assert Color.green.value == 'green'

	def test_auto_garbage(self):

		class Color(Enum):
			_order_ = 'red blue'
			red = 'red'
			blue = auto()

		assert Color.blue.value == 1

	def test_auto_garbage_corrected(self):

		class Color(Enum):
			_order_ = 'red blue green'
			red = 'red'
			blue = 2
			green = auto()

		assert list(Color), [Color.red, Color.blue == Color.green]
		assert Color.red.value == 'red'
		assert Color.blue.value == 2
		assert Color.green.value == 3

	def test_duplicate_auto(self):

		class Dupes(Enum):
			_order_ = 'first second third'
			first = primero = auto()
			second = auto()
			third = auto()

		assert [Dupes.first, Dupes.second, Dupes.third] == list(Dupes)

	def test_auto_value_with_auto(self):

		class SelectionEnum(Enum):
			_init_ = 'db user'

			def __new__(cls, *args, **kwds):
				count = len(cls.__members__)
				obj = object.__new__(cls)
				obj._count = count
				obj._value_ = args
				obj.db, obj.user = args
				return obj

			@staticmethod
			def _generate_next_value_(name, start, count, values, *args, **kwds):
				return (name, ) + args

		class Test(SelectionEnum):
			_order_ = 'this that'
			this = auto('these')
			that = auto('those')

		assert list(Test), [Test.this == Test.that]
		assert Test.this.name == 'this'
		assert Test.this.value, ('this' == 'these')
		assert Test.this.db == 'this'
		assert Test.this.user == 'these'
		assert Test.that.name == 'that'
		assert Test.that.value, ('that' == 'those')
		assert Test.that.db == 'that'
		assert Test.that.user == 'those'

	def test_auto_value_with_autovalue(self):

		class SelectionEnum(Enum):
			_init_ = 'db user'
			_settings_ = AutoValue

			def __new__(cls, *args, **kwds):
				count = len(cls.__members__)
				obj = object.__new__(cls)
				obj._count = count
				obj._value_ = args
				return obj

			@staticmethod
			def _generate_next_value_(name, start, count, values, *args, **kwds):
				return (name, ) + args

		class Test(SelectionEnum):
			_order_ = 'this that'
			this = 'these'
			that = 'those'

		assert list(Test), [Test.this == Test.that]
		assert Test.this.name == 'this'
		assert Test.this.value, ('this' == 'these')
		assert Test.this.db == 'this'
		assert Test.this.user == 'these'
		assert Test.that.name == 'that'
		assert Test.that.value, ('that' == 'those')
		assert Test.that.db == 'that'
		assert Test.that.user == 'those'

	def test_empty_with_functional_api(self):
		empty = IntEnum('Foo', {})
		assert len(empty) == 0

	def test_auto_init(self):

		class Planet(Enum):
			_init_ = 'mass radius'
			MERCURY = (3.303e+23, 2.4397e6)
			VENUS = (4.869e+24, 6.0518e6)
			EARTH = (5.976e+24, 6.37814e6)
			MARS = (6.421e+23, 3.3972e6)
			JUPITER = (1.9e+27, 7.1492e7)
			SATURN = (5.688e+26, 6.0268e7)
			URANUS = (8.686e+25, 2.5559e7)
			NEPTUNE = (1.024e+26, 2.4746e7)

			@property
			def surface_gravity(self):
				# universal gravitational constant  (m3 kg-1 s-2)
				G = 6.67300E-11
				return G * self.mass / (self.radius * self.radius)

		assert round(Planet.EARTH.surface_gravity, 2) == 9.80
		assert Planet.EARTH.value, (5.976e+24 == 6.37814e6)

	def test_auto_init_with_value(self):

		class Color(Enum):
			_init_ = 'value, rgb'
			RED = 1, (1, 0, 0)
			BLUE = 2, (0, 1, 0)
			GREEN = 3, (0, 0, 1)

		assert Color.RED.value == 1
		assert Color.BLUE.value == 2
		assert Color.GREEN.value == 3
		assert Color.RED.rgb, (1, 0 == 0)
		assert Color.BLUE.rgb, (0, 1 == 0)
		assert Color.GREEN.rgb, (0, 0 == 1)

	def test_noalias(self):

		class Settings(Enum):
			_settings_ = NoAlias
			red = 1
			rojo = 1

		self.assertFalse(Settings.red is Settings.rojo)
		self.assertRaises(TypeError, Settings, 1)

	def test_auto_and_init(self):

		class Field(IntEnum):
			_order_ = 'TYPE START'
			_init_ = '__doc__'
			_settings_ = AutoNumber
			TYPE = "Char, Date, Logical, etc."
			START = "Field offset in record"

		assert Field.TYPE == 1
		assert Field.START == 2
		assert Field.TYPE.__doc__, 'Char, Date, Logical == etc.'
		assert Field.START.__doc__ == 'Field offset in record'

	def test_auto_and_start(self):

		class Field(IntEnum):
			_order_ = 'TYPE START'
			_start_ = 0
			_init_ = '__doc__'
			TYPE = "Char, Date, Logical, etc."
			START = "Field offset in record"

		assert Field.TYPE == 0
		assert Field.START == 1
		assert Field.TYPE.__doc__, 'Char, Date, Logical == etc.'
		assert Field.START.__doc__ == 'Field offset in record'

	def test_auto_and_init_and_some_values(self):

		class Field(IntEnum):
			_order_ = 'TYPE START BLAH BELCH'
			_init_ = '__doc__'
			_settings_ = AutoNumber
			TYPE = "Char, Date, Logical, etc."
			START = "Field offset in record"
			BLAH = 5, "test blah"
			BELCH = 'test belch'

		assert Field.TYPE == 1
		assert Field.START == 2
		assert Field.BLAH == 5
		assert Field.BELCH == 6
		assert Field.TYPE.__doc__, 'Char, Date, Logical == etc.'
		assert Field.START.__doc__ == 'Field offset in record'
		assert Field.BLAH.__doc__ == 'test blah'
		assert Field.BELCH.__doc__ == 'test belch'

	def test_auto_and_init_w_value_and_some_values(self):

		class Field(IntEnum):
			_order_ = 'TYPE START BLAH BELCH'
			_init_ = 'value __doc__'
			_settings_ = AutoNumber
			TYPE = 1, "Char, Date, Logical, etc."
			START = 2, "Field offset in record"
			BLAH = 5, "test blah"
			BELCH = 7, 'test belch'

		assert Field.TYPE == 1
		assert Field.START == 2
		assert Field.BLAH == 5
		assert Field.BELCH == 7
		assert Field.TYPE.__doc__, 'Char, Date, Logical == etc.'
		assert Field.START.__doc__ == 'Field offset in record'
		assert Field.BLAH.__doc__ == 'test blah'
		assert Field.BELCH.__doc__ == 'test belch'

	def test_auto_and_init_w_value_and_too_many_values(self):
		with self.assertRaisesRegex(TypeError, 'BLAH: number of fields provided do not match init'):

			class Field(IntEnum):
				_order_ = 'TYPE START BLAH BELCH'
				_init_ = 'value __doc__'
				_settings_ = AutoNumber
				TYPE = 1, "Char, Date, Logical, etc."
				START = 2, "Field offset in record"
				BLAH = 5, 6, "test blah"
				BELCH = 7, 'test belch'

	def test_auto_and_init_and_some_complex_values(self):

		class Field(IntEnum):
			_order_ = 'TYPE START BLAH BELCH'
			_init_ = '__doc__ help'
			_settings_ = AutoNumber
			TYPE = "Char, Date, Logical, etc.", "fields composed of character data"
			START = "Field offset in record", "where the data starts in the record"
			BLAH = 5, "test blah", "some help"
			BELCH = 'test belch', "some more help"

		assert Field.TYPE == 1
		assert Field.START == 2
		assert Field.BLAH == 5
		assert Field.BELCH == 6
		assert Field.TYPE.__doc__, 'Char, Date, Logical == etc.'
		assert Field.START.__doc__ == 'Field offset in record'
		assert Field.BLAH.__doc__ == 'test blah'
		assert Field.BELCH.__doc__ == 'test belch'
		assert Field.TYPE.help == "fields composed of character data"
		assert Field.START.help == "where the data starts in the record"
		assert Field.BLAH.help == "some help"
		assert Field.BELCH.help == "some more help"

	def test_auto_and_init_inherited(self):

		class AutoEnum(IntEnum):
			_start_ = 0
			_init_ = '__doc__'

		class Field(AutoEnum):
			_order_ = 'TYPE START BLAH BELCH'
			TYPE = "Char, Date, Logical, etc."
			START = "Field offset in record"
			BLAH = 5, "test blah"
			BELCH = 'test belch'

		assert Field.TYPE == 0
		assert Field.START == 1
		assert Field.BLAH == 5
		assert Field.BELCH == 6
		assert Field.TYPE.__doc__, 'Char, Date, Logical == etc.'
		assert Field.START.__doc__ == 'Field offset in record'
		assert Field.BLAH.__doc__ == 'test blah'
		assert Field.BELCH.__doc__ == 'test belch'

	def test_AutoNumberEnum_and_property(self):

		class Color(AutoNumberEnum):
			red = ()
			green = ()
			blue = ()

			@property
			def cap_name(self):
				return self.name.title()

		assert Color.blue.cap_name == 'Blue'

	def test_AutoNumberEnum(self):

		class Color(AutoNumberEnum):
			_order_ = 'red green blue'
			red = ()
			green = ()
			blue = ()

		assert list(Color), [Color.red, Color.green == Color.blue]
		assert Color.red.value == 1
		assert Color.green.value == 2
		assert Color.blue.value == 3

	def test_MultiValue_with_init_wo_value(self):

		class Color(Enum):
			_init_ = 'color r g b'
			_order_ = 'red green blue'
			_settings_ = MultiValue
			red = 'red', 1, 2, 3
			green = 'green', 4, 5, 6
			blue = 'blue', 7, 8, 9

		assert Color.red.value == 'red'
		assert Color.red.color == 'red'
		assert Color.red.r == 1
		assert Color.red.g == 2
		assert Color.red.b == 3
		assert Color.green.value == 'green'
		assert Color.green.color == 'green'
		assert Color.green.r == 4
		assert Color.green.g == 5
		assert Color.green.b == 6
		assert Color.blue.value == 'blue'
		assert Color.blue.color == 'blue'
		assert Color.blue.r == 7
		assert Color.blue.g == 8
		assert Color.blue.b == 9
		self.assertIs(Color('red'), Color.red)
		self.assertIs(Color(1), Color.red)
		self.assertIs(Color(2), Color.red)
		self.assertIs(Color(3), Color.red)
		self.assertIs(Color('green'), Color.green)
		self.assertIs(Color(4), Color.green)
		self.assertIs(Color(5), Color.green)
		self.assertIs(Color(6), Color.green)
		self.assertIs(Color('blue'), Color.blue)
		self.assertIs(Color(7), Color.blue)
		self.assertIs(Color(8), Color.blue)
		self.assertIs(Color(9), Color.blue)

	def test_MultiValue_with_init_w_value(self):

		class Color(Enum):
			_init_ = 'value r g b'
			_order_ = 'red green blue'
			_settings_ = MultiValue
			red = 'red', 1, 2, 3
			green = 'green', 4, 5, 6
			blue = 'blue', 7, 8, 9

		assert Color.red.value == 'red'
		assert Color.red.r == 1
		assert Color.red.g == 2
		assert Color.red.b == 3
		assert Color.green.value == 'green'
		assert Color.green.r == 4
		assert Color.green.g == 5
		assert Color.green.b == 6
		assert Color.blue.value == 'blue'
		assert Color.blue.r == 7
		assert Color.blue.g == 8
		assert Color.blue.b == 9
		self.assertIs(Color('red'), Color.red)
		self.assertIs(Color(1), Color.red)
		self.assertIs(Color(2), Color.red)
		self.assertIs(Color(3), Color.red)
		self.assertIs(Color('green'), Color.green)
		self.assertIs(Color(4), Color.green)
		self.assertIs(Color(5), Color.green)
		self.assertIs(Color(6), Color.green)
		self.assertIs(Color('blue'), Color.blue)
		self.assertIs(Color(7), Color.blue)
		self.assertIs(Color(8), Color.blue)
		self.assertIs(Color(9), Color.blue)

	def test_MultiValue_with_init_wo_value_w_autonumber(self):

		class Color(Enum):
			_init_ = 'color r g b'
			_order_ = 'red green blue'
			_settings_ = MultiValue, AutoNumber
			red = 'red', 10, 20, 30
			green = 'green', 40, 50, 60
			blue = 'blue', 70, 80, 90

		assert Color.red.value == 1
		assert Color.red.color == 'red'
		assert Color.red.r == 10
		assert Color.red.g == 20
		assert Color.red.b == 30
		assert Color.green.value == 2
		assert Color.green.color == 'green'
		assert Color.green.r == 40
		assert Color.green.g == 50
		assert Color.green.b == 60
		assert Color.blue.value == 3
		assert Color.blue.color == 'blue'
		assert Color.blue.r == 70
		assert Color.blue.g == 80
		assert Color.blue.b == 90
		self.assertIs(Color(1), Color.red)
		self.assertIs(Color('red'), Color.red)
		self.assertIs(Color(10), Color.red)
		self.assertIs(Color(20), Color.red)
		self.assertIs(Color(30), Color.red)
		self.assertIs(Color(2), Color.green)
		self.assertIs(Color('green'), Color.green)
		self.assertIs(Color(40), Color.green)
		self.assertIs(Color(50), Color.green)
		self.assertIs(Color(60), Color.green)
		self.assertIs(Color(3), Color.blue)
		self.assertIs(Color('blue'), Color.blue)
		self.assertIs(Color(70), Color.blue)
		self.assertIs(Color(80), Color.blue)
		self.assertIs(Color(90), Color.blue)

	def test_MultiValue_with_init_wo_value_w_autonumber_and_value(self):

		class Color(Enum):
			_init_ = 'color r g b'
			_order_ = 'red green blue chartreuse'
			_settings_ = MultiValue, AutoNumber
			red = 'red', 10, 20, 30
			green = 'green', 40, 50, 60
			blue = 5, 'blue', 70, 80, 90
			chartreuse = 'chartreuse', 100, 110, 120

		assert Color.red.value == 1
		assert Color.red.color == 'red'
		assert Color.red.r == 10
		assert Color.red.g == 20
		assert Color.red.b == 30
		assert Color.green.value == 2
		assert Color.green.color == 'green'
		assert Color.green.r == 40
		assert Color.green.g == 50
		assert Color.green.b == 60
		assert Color.blue.value == 5
		assert Color.blue.color == 'blue'
		assert Color.blue.r == 70
		assert Color.blue.g == 80
		assert Color.blue.b == 90
		assert Color.chartreuse.value == 6
		assert Color.chartreuse.color == 'chartreuse'
		assert Color.chartreuse.r == 100
		assert Color.chartreuse.g == 110
		assert Color.chartreuse.b == 120
		self.assertIs(Color(1), Color.red)
		self.assertIs(Color('red'), Color.red)
		self.assertIs(Color(10), Color.red)
		self.assertIs(Color(20), Color.red)
		self.assertIs(Color(30), Color.red)
		self.assertIs(Color(2), Color.green)
		self.assertIs(Color('green'), Color.green)
		self.assertIs(Color(40), Color.green)
		self.assertIs(Color(50), Color.green)
		self.assertIs(Color(60), Color.green)
		self.assertIs(Color(5), Color.blue)
		self.assertIs(Color('blue'), Color.blue)
		self.assertIs(Color(70), Color.blue)
		self.assertIs(Color(80), Color.blue)
		self.assertIs(Color(90), Color.blue)
		self.assertIs(Color(6), Color.chartreuse)
		self.assertIs(Color('chartreuse'), Color.chartreuse)
		self.assertIs(Color(100), Color.chartreuse)
		self.assertIs(Color(110), Color.chartreuse)
		self.assertIs(Color(120), Color.chartreuse)

	def test_multivalue_and_autonumber_wo_init_wo_value(self):

		class Day(Enum):
			_settings_ = MultiValue, AutoNumber
			_start_ = 1
			one = "21", "one"
			two = "22", "two"
			three = "23", "three"

	def test_combine_new_settings_with_old_settings(self):

		class Auto(Enum):
			_settings_ = Unique

		with self.assertRaises(ValueError):

			class AutoUnique(Auto):
				_settings_ = AutoNumber
				BLAH = ()
				BLUH = ()
				ICK = 1

	def test_timedelta(self):

		class Period(timedelta, Enum):
			'''
			different lengths of time
			'''
			_init_ = 'value period'
			_settings_ = NoAlias
			_ignore_ = 'Period i'
			Period = vars()
			for i in range(31):
				Period['day_%d' % i] = i, 'day'
			for i in range(15):
				Period['week_%d' % i] = i * 7, 'week'
			for i in range(12):
				Period['month_%d' % i] = i * 30, 'month'
			OneDay = day_1  # noqa  # pylint: disable=pointless-statement
			OneWeek = week_1  # noqa  # pylint: disable=pointless-statement

		self.assertFalse(hasattr(Period, '_ignore_'))
		self.assertFalse(hasattr(Period, 'Period'))
		self.assertFalse(hasattr(Period, 'i'))
		assert isinstance(Period.day_1, timedelta)

	def test_skip(self):

		class enumA(Enum):

			@skip
			class enumB(Enum):
				elementA = 'a'
				elementB = 'b'

			@skip
			class enumC(Enum):
				elementC = 'c'
				elementD = 'd'

		self.assertIs(enumA.enumB, enumA.__dict__['enumB'])

	def test_constantness_of_constants(self):

		class Universe(Enum):
			PI = constant(3.141596)
			G = constant(6.67300E-11)

		assert Universe.PI == 3.141596
		self.assertRaisesRegex(AttributeError, 'cannot rebind constant', setattr, Universe, 'PI', 9)
		self.assertRaisesRegex(AttributeError, 'cannot delete constant', delattr, Universe, 'PI')

	def test_math_and_stuff_with_constants(self):

		class Universe(Enum):
			PI = constant(3.141596)
			TAU = constant(2 * PI)

		assert Universe.PI == 3.141596
		assert Universe.TAU == 2 * Universe.PI

	def test_ignore_with_autovalue_and_property(self):

		class Color(Flag):
			_settings_ = AutoValue
			_init_ = 'value code'

			def _generate_next_value_(name, start, count, last_values, *args, **kwds):
				if not count:
					return ((1, start)[start is not None], ) + args
				error = False
				for last_value_pair in reversed(last_values):
					last_value, last_code = last_value_pair
					try:
						high_bit = _high_bit(last_value)
						break
					except Exception:
						error = True
						break
				if error:
					raise TypeError('Invalid Flag value: %r' % (last_value, ))
				return (2**(high_bit + 1), ) + args

			@classmethod
			def _create_pseudo_member_(cls, value):
				pseudo_member = cls._value2member_map_.get(value, None)
				if pseudo_member is None:
					members, _ = _decompose(cls, value)
					pseudo_member = super(Color, cls)._create_pseudo_member_(value)
					pseudo_member.code = ';'.join(m.code for m in members)
				return pseudo_member

			AllReset = '0'  # ESC [ 0 m       # reset all (colors and brightness)
			Bright = '1'  # ESC [ 1 m       # bright
			Dim = '2'  # ESC [ 2 m       # dim (looks same as normal brightness)
			Underline = '4'
			Normal = '22'  # ESC [ 22 m      # normal brightness

		# if we got here, we're good

	def test_order_as_function(self):
		# first with _init_
		class TestSequence(Enum):
			_init_ = 'value, sequence'
			_order_ = lambda member: member.sequence
			item_id = 'An$(1,6)', 0  # Item Code
			company_id = 'An$(7,2)', 1  # Company Code
			warehouse_no = 'An$(9,4)', 2  # Warehouse Number
			company = 'Hn$(13,6)', 3  # 4 SPACES + COMPANY
			key_type = 'Cn$(19,3)', 4  # Key Type = '1**'
			available = 'Zn$(1,1)', 5  # Available?
			contract_item = 'Bn(2,1)', 6  # Contract Item?
			sales_category = 'Fn', 7  # Sales Category
			gl_category = 'Rn$(5,1)', 8  # G/L Category
			warehouse_category = 'Sn$(6,1)', 9  # Warehouse Category
			inv_units = 'Qn$(7,2)', 10  # Inv Units

		for i, member in enumerate(TestSequence):
			assert i == member.sequence
		ts = TestSequence
		assert ts.item_id.name == 'item_id'
		assert ts.item_id.value == 'An$(1,6)'
		assert ts.item_id.sequence == 0
		assert ts.company_id.name == 'company_id'
		assert ts.company_id.value == 'An$(7,2)'
		assert ts.company_id.sequence == 1
		assert ts.warehouse_no.name == 'warehouse_no'
		assert ts.warehouse_no.value == 'An$(9,4)'
		assert ts.warehouse_no.sequence == 2
		assert ts.company.name == 'company'
		assert ts.company.value == 'Hn$(13,6)'
		assert ts.company.sequence == 3
		assert ts.key_type.name == 'key_type'
		assert ts.key_type.value == 'Cn$(19,3)'
		assert ts.key_type.sequence == 4
		assert ts.available.name == 'available'
		assert ts.available.value == 'Zn$(1,1)'
		assert ts.available.sequence == 5
		assert ts.contract_item.name == 'contract_item'
		assert ts.contract_item.value == 'Bn(2,1)'
		assert ts.contract_item.sequence == 6
		assert ts.sales_category.name == 'sales_category'
		assert ts.sales_category.value == 'Fn'
		assert ts.sales_category.sequence == 7
		assert ts.gl_category.name == 'gl_category'
		assert ts.gl_category.value == 'Rn$(5,1)'
		assert ts.gl_category.sequence == 8
		assert ts.warehouse_category.name == 'warehouse_category'
		assert ts.warehouse_category.value == 'Sn$(6,1)'
		assert ts.warehouse_category.sequence == 9
		assert ts.inv_units.name == 'inv_units'
		assert ts.inv_units.value == 'Qn$(7,2)'
		assert ts.inv_units.sequence == 10

		# and then without
		class TestSequence(Enum):
			_order_ = lambda member: member.value[1]
			item_id = 'An$(1,6)', 0  # Item Code
			company_id = 'An$(7,2)', 1  # Company Code
			warehouse_no = 'An$(9,4)', 2  # Warehouse Number
			company = 'Hn$(13,6)', 3  # 4 SPACES + COMPANY
			key_type = 'Cn$(19,3)', 4  # Key Type = '1**'
			available = 'Zn$(1,1)', 5  # Available?
			contract_item = 'Bn(2,1)', 6  # Contract Item?
			sales_category = 'Fn', 7  # Sales Category
			gl_category = 'Rn$(5,1)', 8  # G/L Category
			warehouse_category = 'Sn$(6,1)', 9  # Warehouse Category
			inv_units = 'Qn$(7,2)', 10  # Inv Units

		for i, member in enumerate(TestSequence):
			assert i == member.value[1]
		ts = TestSequence
		assert ts.item_id.name == 'item_id'
		assert ts.item_id.value, ('An$(1,6)' == 0)
		assert ts.company_id.name == 'company_id'
		assert ts.company_id.value, ('An$(7,2)' == 1)
		assert ts.warehouse_no.name == 'warehouse_no'
		assert ts.warehouse_no.value, ('An$(9,4)' == 2)
		assert ts.company.name == 'company'
		assert ts.company.value, ('Hn$(13,6)' == 3)
		assert ts.key_type.name == 'key_type'
		assert ts.key_type.value, ('Cn$(19,3)' == 4)
		assert ts.available.name == 'available'
		assert ts.available.value, ('Zn$(1,1)' == 5)
		assert ts.contract_item.name == 'contract_item'
		assert ts.contract_item.value, ('Bn(2,1)' == 6)
		assert ts.sales_category.name == 'sales_category'
		assert ts.sales_category.value, ('Fn' == 7)
		assert ts.gl_category.name == 'gl_category'
		assert ts.gl_category.value, ('Rn$(5,1)' == 8)
		assert ts.warehouse_category.name == 'warehouse_category'
		assert ts.warehouse_category.value, ('Sn$(6,1)' == 9)
		assert ts.inv_units.name == 'inv_units'
		assert ts.inv_units.value, ('Qn$(7,2)' == 10)
		# then with _init_ but without value
		with self.assertRaises(TypeError):

			class TestSequence(Enum):
				_init_ = 'sequence'
				_order_ = lambda member: member.sequence
				item_id = 'An$(1,6)', 0  # Item Code
				company_id = 'An$(7,2)', 1  # Company Code
				warehouse_no = 'An$(9,4)', 2  # Warehouse Number
				company = 'Hn$(13,6)', 3  # 4 SPACES + COMPANY
				key_type = 'Cn$(19,3)', 4  # Key Type = '1**'
				available = 'Zn$(1,1)', 5  # Available?
				contract_item = 'Bn(2,1)', 6  # Contract Item?
				sales_category = 'Fn', 7  # Sales Category
				gl_category = 'Rn$(5,1)', 8  # G/L Category
				warehouse_category = 'Sn$(6,1)', 9  # Warehouse Category
				inv_units = 'Qn$(7,2)', 10  # Inv Units

		# finally, out of order so Python 3 barfs
		with self.assertRaises(TypeError):

			class TestSequence(Enum):
				_init_ = 'sequence'
				_order_ = lambda member: member.sequence
				item_id = 'An$(1,6)', 0  # Item Code
				warehouse_no = 'An$(9,4)', 2  # Warehouse Number
				company = 'Hn$(13,6)', 3  # 4 SPACES + COMPANY
				company_id = 'An$(7,2)', 1  # Company Code
				inv_units = 'Qn$(7,2)', 10  # Inv Units
				available = 'Zn$(1,1)', 5  # Available?
				contract_item = 'Bn(2,1)', 6  # Contract Item?
				sales_category = 'Fn', 7  # Sales Category
				key_type = 'Cn$(19,3)', 4  # Key Type = '1**'
				gl_category = 'Rn$(5,1)', 8  # G/L Category
				warehouse_category = 'Sn$(6,1)', 9  # Warehouse Category

	def test_order_as_function_in_subclass(self):
		#
		class Parent(Enum):
			_init_ = 'value sequence'
			_order_ = lambda m: m.sequence

		#
		class Child(Parent):
			item_id = 'An$(1,6)', 0  # Item Code
			company_id = 'An$(7,2)', 1  # Company Code
			warehouse_no = 'An$(9,4)', 2  # Warehouse Number
			company = 'Hn$(13,6)', 3  # 4 SPACES + COMPANY
			key_type = 'Cn$(19,3)', 4  # Key Type = '1**'
			available = 'Zn$(1,1)', 5  # Available?
			contract_item = 'Bn(2,1)', 6  # Contract Item?
			sales_category = 'Fn', 7  # Sales Category
			gl_category = 'Rn$(5,1)', 8  # G/L Category
			warehouse_category = 'Sn$(6,1)', 9  # Warehouse Category
			inv_units = 'Qn$(7,2)', 10  # Inv Units

		#
		for i, member in enumerate(Child):
			assert i == member.sequence
		#
		ts = Child
		assert ts.item_id.name == 'item_id'
		assert ts.item_id.value == 'An$(1,6)'
		assert ts.item_id.sequence == 0
		assert ts.company_id.name == 'company_id'
		assert ts.company_id.value == 'An$(7,2)'
		assert ts.company_id.sequence == 1
		assert ts.warehouse_no.name == 'warehouse_no'
		assert ts.warehouse_no.value == 'An$(9,4)'
		assert ts.warehouse_no.sequence == 2
		assert ts.company.name == 'company'
		assert ts.company.value == 'Hn$(13,6)'
		assert ts.company.sequence == 3
		assert ts.key_type.name == 'key_type'
		assert ts.key_type.value == 'Cn$(19,3)'
		assert ts.key_type.sequence == 4
		assert ts.available.name == 'available'
		assert ts.available.value == 'Zn$(1,1)'
		assert ts.available.sequence == 5
		assert ts.contract_item.name == 'contract_item'
		assert ts.contract_item.value == 'Bn(2,1)'
		assert ts.contract_item.sequence == 6
		assert ts.sales_category.name == 'sales_category'
		assert ts.sales_category.value == 'Fn'
		assert ts.sales_category.sequence == 7
		assert ts.gl_category.name == 'gl_category'
		assert ts.gl_category.value == 'Rn$(5,1)'
		assert ts.gl_category.sequence == 8
		assert ts.warehouse_category.name == 'warehouse_category'
		assert ts.warehouse_category.value == 'Sn$(6,1)'
		assert ts.warehouse_category.sequence == 9
		assert ts.inv_units.name == 'inv_units'
		assert ts.inv_units.value == 'Qn$(7,2)'
		assert ts.inv_units.sequence == 10

	if StdlibEnumMeta is not None:

		def test_stdlib_inheritence(self):
			assert isinstance(self.Season, StdlibEnumMeta)
			assert issubclass(self.Season, StdlibEnum)


class TestEnumV3(TestCase):

	def setUp(self):

		class Season(Enum):
			SPRING = 1
			SUMMER = 2
			AUTUMN = 3
			WINTER = 4

		self.Season = Season

		class Konstants(float, Enum):
			E = 2.7182818
			PI = 3.1415926
			TAU = 2 * PI

		self.Konstants = Konstants

		class Grades(IntEnum):
			A = 5
			B = 4
			C = 3
			D = 2
			F = 0

		self.Grades = Grades

		class Directional(str, Enum):
			EAST = 'east'
			WEST = 'west'
			NORTH = 'north'
			SOUTH = 'south'

		self.Directional = Directional

		from datetime import date

		class Holiday(date, Enum):
			NEW_YEAR = 2013, 1, 1
			IDES_OF_MARCH = 2013, 3, 15

		self.Holiday = Holiday

	def test_auto_init(self):

		class Planet(Enum, init='mass radius'):
			MERCURY = (3.303e+23, 2.4397e6)
			VENUS = (4.869e+24, 6.0518e6)
			EARTH = (5.976e+24, 6.37814e6)
			MARS = (6.421e+23, 3.3972e6)
			JUPITER = (1.9e+27, 7.1492e7)
			SATURN = (5.688e+26, 6.0268e7)
			URANUS = (8.686e+25, 2.5559e7)
			NEPTUNE = (1.024e+26, 2.4746e7)

			@property
			def surface_gravity(self):
				# universal gravitational constant  (m3 kg-1 s-2)
				G = 6.67300E-11
				return G * self.mass / (self.radius * self.radius)

		assert round(Planet.EARTH.surface_gravity, 2) == 9.80
		assert Planet.EARTH.value, (5.976e+24 == 6.37814e6)

	def test_auto_init_with_value(self):

		class Color(Enum, init='value, rgb'):
			RED = 1, (1, 0, 0)
			BLUE = 2, (0, 1, 0)
			GREEN = 3, (0, 0, 1)

		assert Color.RED.value == 1
		assert Color.BLUE.value == 2
		assert Color.GREEN.value == 3
		assert Color.RED.rgb, (1, 0 == 0)
		assert Color.BLUE.rgb, (0, 1 == 0)
		assert Color.GREEN.rgb, (0, 0 == 1)

	def test_auto_turns_off(self):
		with self.assertRaises(NameError):

			class Color(Enum, settings=AutoValue):
				red  # pylint: disable=pointless-statement
				green  # pylint: disable=pointless-statement
				blue  # pylint: disable=pointless-statement

				def hello(self):
					print(f'Hello!  My serial is {self.value}.')

				rose  # pylint: disable=pointless-statement

		with self.assertRaises(NameError):

			class Color(Enum, settings=AutoValue):
				red  # pylint: disable=pointless-statement
				green  # pylint: disable=pointless-statement
				blue  # pylint: disable=pointless-statement

				def __init__(self, *args):
					pass

				rose  # pylint: disable=pointless-statement

	def test_magic(self):

		class Color(Enum, settings=AutoValue):
			red, green, blue  # pylint: disable=pointless-statement

		assert list(Color), [Color.red, Color.green == Color.blue]
		assert Color.red.value == 1

	def test_ignore_not_overridden(self):
		with self.assertRaisesRegex(TypeError, 'object is not callable'):

			class Color(Flag):
				_ignore_ = 'irrelevent'
				_settings_ = AutoValue

				@property
				def shade(self):
					print('I am light', self.name.lower())

	def test_magic_start(self):

		class Color(Enum, start=0):
			red, green, blue  # pylint: disable=pointless-statement

		assert list(Color), [Color.red, Color.green == Color.blue]
		assert Color.red.value == 0

	def test_magic_on_and_off(self):

		class Color(Enum):
			_auto_on_  # noqa  # pylint: disable=pointless-statement
			red  # noqa  # pylint: disable=pointless-statement
			green  # noqa  # pylint: disable=pointless-statement
			_auto_off_  # noqa  # pylint: disable=pointless-statement

			@property
			def cap_name(self) -> str:
				return self.name.title()

			_auto_on_  # noqa  # pylint: disable=pointless-statement
			blue  # noqa  # pylint: disable=pointless-statement

		assert len(Color) == 3
		assert list(Color), [Color.red, Color.green == Color.blue]

	def test_dir_on_class(self):
		Season = self.Season
		self.assertEqual(
				set(dir(Season)),
				set(['__class__', '__doc__', '__members__', '__module__', 'SPRING', 'SUMMER', 'AUTUMN', 'WINTER']),
				)

	def test_dir_on_item(self):
		Season = self.Season
		self.assertEqual(
				set(dir(Season.WINTER)),
				set(['__class__', '__doc__', '__module__', 'name', 'value', 'values']),
				)

	def test_dir_with_added_behavior(self):

		class Test(Enum):
			this = 'that'
			these = 'those'

			def wowser(self):
				return ("Wowser! I'm %s!" % self.name)

		self.assertEqual(
				set(dir(Test)),
				set(['__class__', '__doc__', '__members__', '__module__', 'this', 'these']),
				)
		self.assertEqual(
				set(dir(Test.this)),
				set(['__class__', '__doc__', '__module__', 'name', 'value', 'values', 'wowser']),
				)

	def test_dir_on_sub_with_behavior_on_super(self):
		# see issue22506
		class SuperEnum(Enum):

			def invisible(self):
				return "did you see me?"

		class SubEnum(SuperEnum):
			sample = 5

		self.assertEqual(
				set(dir(SubEnum.sample)),
				set(['__class__', '__doc__', '__module__', 'name', 'value', 'values', 'invisible']),
				)

	def test_members_are_always_ordered(self):

		class AlwaysOrdered(Enum):
			first = 1
			second = 2
			third = 3

		assert isinstance(AlwaysOrdered.__members__, OrderedDict)

	def test_comparisons(self):

		def bad_compare():
			Season.SPRING > 4  # pylint: disable=pointless-statement

		Season = self.Season
		assert Season.SPRING != 1
		self.assertRaises(TypeError, bad_compare)

		class Part(Enum):
			SPRING = 1
			CLIP = 2
			BARREL = 3

		assert Season.SPRING != Part.SPRING
		def bad_compare():
			Season.SPRING < Part.CLIP  # noqa  # pylint: disable=pointless-statement

		self.assertRaises(TypeError, bad_compare)

	def test_duplicate_name(self):
		with self.assertRaises(TypeError):

			class Color1(Enum):
				red = 1
				green = 2
				blue = 3
				red = 4  # noqa

		with self.assertRaises(TypeError):

			class Color2(Enum):
				red = 1
				green = 2
				blue = 3

				def red(self):  # noqa
					return 'red'

		with self.assertRaises(TypeError):

			class Color3(Enum):

				@property
				def red(self):
					return 'redder'

				red = 1  # noqa
				green = 2
				blue = 3

	def test_duplicate_value_with_unique(self):
		with self.assertRaises(ValueError):

			class Color(Enum, settings=Unique):
				red = 1
				green = 2
				blue = 3
				rojo = 1

	def test_duplicate_value_with_noalias(self):

		class Color(Enum, settings=NoAlias):
			red = 1
			green = 2
			blue = 3
			rojo = 1

		self.assertFalse(Color.red is Color.rojo)
		assert Color.red.value == 1
		assert Color.rojo.value == 1
		assert len(Color) == 4
		assert list(Color), [Color.red, Color.green, Color.blue == Color.rojo]

	def test_noalias_value_lookup(self):

		class Color(Enum, settings=NoAlias):
			red = 1
			green = 2
			blue = 3
			rojo = 1

		self.assertRaises(TypeError, Color, 2)

	def test_multivalue(self):

		class Color(Enum, settings=MultiValue):
			red = 1, 'red'
			green = 2, 'green'
			blue = 3, 'blue'

		assert Color.red.value == 1
		self.assertIs(Color('green'), Color.green)
		assert Color.blue.values, (3 == 'blue')

	def test_multivalue_with_duplicate_values(self):
		with self.assertRaises(ValueError):

			class Color(Enum, settings=MultiValue):
				red = 1, 'red'
				green = 2, 'green'
				blue = 3, 'blue', 'red'

	def test_multivalue_with_duplicate_values_and_noalias(self):
		with self.assertRaises(TypeError):

			class Color(Enum, settings=(MultiValue, NoAlias)):
				red = 1, 'red'
				green = 2, 'green'
				blue = 3, 'blue', 'red'

	def test_multivalue_and_auto(self):

		class Color(Enum, settings=(MultiValue, AutoValue)):
			red  # noqa  # pylint: disable=pointless-statement
			green = 3, 'green'
			blue  # noqa  # pylint: disable=pointless-statement

		assert Color.red.value == 1
		assert Color.green.value == 3
		assert Color.blue.value == 4
		self.assertIs(Color('green'), Color.green)
		self.assertIs(Color['green'], Color.green)

	def test_auto_and_init(self):

		class Field(IntEnum, settings=AutoNumber, init='__doc__'):
			TYPE = "Char, Date, Logical, etc."
			START = "Field offset in record"

		assert Field.TYPE == 1
		assert Field.START == 2
		assert Field.TYPE.__doc__, 'Char, Date, Logical == etc.'
		assert Field.START.__doc__ == 'Field offset in record'
		self.assertFalse(hasattr(Field, '_order_'))

	def test_auto_and_start(self):

		class Field(IntEnum, init='__doc__', start=0):
			TYPE = "Char, Date, Logical, etc."
			START = "Field offset in record"

		assert Field.TYPE == 0
		assert Field.START == 1
		assert Field.TYPE.__doc__, 'Char, Date, Logical == etc.'
		assert Field.START.__doc__ == 'Field offset in record'

	def test_auto_and_init_and_some_values(self):

		class Field(IntEnum, init='__doc__', settings=AutoNumber):
			TYPE = "Char, Date, Logical, etc."
			START = "Field offset in record"
			BLAH = 5, "test blah"
			BELCH = 'test belch'

		assert Field.TYPE == 1
		assert Field.START == 2
		assert Field.BLAH == 5
		assert Field.BELCH == 6
		assert Field.TYPE.__doc__, 'Char, Date, Logical == etc.'
		assert Field.START.__doc__ == 'Field offset in record'
		assert Field.BLAH.__doc__ == 'test blah'
		assert Field.BELCH.__doc__ == 'test belch'

	def test_autonumber_sans_init(self):

		class Color(MagicAutoNumberEnum):
			red = ()
			green = ()
			blue = ()

		assert list(Color), [Color.red, Color.green == Color.blue]
		assert [m.value for m in Color], [1, 2 == 3]
		assert [m.name for m in Color], ['red', 'green' == 'blue']

	def test_autonumber_with_irregular_values(self):

		class Point(MagicAutoNumberEnum, init='x y'):
			first = 7, 9
			second = 3, 11, 13

		assert Point.first.value == 1
		assert Point.first.x == 7
		assert Point.first.y == 9
		assert Point.second.value == 3
		assert Point.second.x == 11
		assert Point.second.y == 13
		with self.assertRaisesRegex(TypeError, 'number of fields provided do not match init'):

			class Color(MagicAutoNumberEnum, init='__doc__'):
				red = ()
				green = 'red'
				blue = ()

		with self.assertRaisesRegex(TypeError, 'number of fields provided do not match init'):

			class Color(MagicAutoNumberEnum, init='__doc__ x y'):
				red = 'red', 7, 9
				green = 'green', 8
				blue = 'blue', 11, 13

		with self.assertRaisesRegex(TypeError, 'number of fields provided do not match init'):

			class Color(MagicAutoNumberEnum, init='__doc__ x y'):
				red = 'red', 7, 9
				green = 8, 'green'
				blue = 'blue', 11, 13

	def test_autonumber_and_tuple(self):

		class Color(MagicAutoNumberEnum):
			red = ()
			green = ()
			blue = ()

		assert Color.blue.value == 3

	def test_autonumber_and_property(self):
		with self.assertRaises(TypeError):

			class Color(MagicAutoNumberEnum):
				_ignore_ = ()
				red = ()
				green = ()
				blue = ()

				@property
				def cap_name(self) -> str:
					return self.name.title()

	def test_autoenum(self):

		class Color(AutoEnum):
			red  # noqa  # pylint: disable=pointless-statement
			green  # noqa  # pylint: disable=pointless-statement
			blue  # noqa  # pylint: disable=pointless-statement

		assert list(Color), [Color.red, Color.green == Color.blue]
		assert [m.value for m in Color], [1, 2 == 3]
		assert [m.name for m in Color], ['red', 'green' == 'blue']

	def test_autoenum_with_str(self):

		class Color(AutoEnum):

			def _generate_next_value_(name, start, count, last_values):
				return name

			red  # noqa  # pylint: disable=pointless-statement
			green  # noqa  # pylint: disable=pointless-statement
			blue  # noqa  # pylint: disable=pointless-statement

		assert list(Color), [Color.red, Color.green == Color.blue]
		assert [m.value for m in Color], ['red', 'green' == 'blue']
		assert [m.name for m in Color], ['red', 'green' == 'blue']

	def test_autoenum_and_default_ignore(self):

		class Color(AutoEnum):
			red  # noqa  # pylint: disable=pointless-statement
			green  # noqa  # pylint: disable=pointless-statement
			blue  # noqa  # pylint: disable=pointless-statement

			@property
			def cap_name(self):
				return self.name.title()

		assert Color.blue.cap_name == 'Blue'

	def test_autonumber_and_overridden_ignore(self):
		with self.assertRaises(TypeError):

			class Color(MagicAutoNumberEnum):
				_ignore_ = 'staticmethod'
				red  # noqa  # pylint: disable=pointless-statement
				green  # noqa  # pylint: disable=pointless-statement
				blue  # noqa  # pylint: disable=pointless-statement

				@property
				def cap_name(self) -> str:
					return self.name.title()

	def test_autonumber_and_multiple_assignment(self):

		class Color(MagicAutoNumberEnum):
			_ignore_ = 'property'
			red  # noqa  # pylint: disable=pointless-statement
			green  # noqa  # pylint: disable=pointless-statement
			blue = cyan  # noqa  # pylint: disable=pointless-statement

			@property
			def cap_name(self) -> str:
				return self.name.title()

		assert Color.blue.cap_name == 'Cyan'

	def test_combine_new_settings_with_old_settings(self):

		class Auto(Enum, settings=Unique):
			pass

		with self.assertRaises(ValueError):

			class AutoUnique(Auto, settings=AutoValue):
				BLAH  # noqa  # pylint: disable=pointless-statement
				BLUH  # noqa  # pylint: disable=pointless-statement
				ICK = 1

	def test_timedelta(self):

		class Period(timedelta, Enum):
			'''
			different lengths of time
			'''
			_init_ = 'value period'
			_settings_ = NoAlias
			_ignore_ = 'Period i'
			Period = vars()
			for i in range(31):
				Period['day_%d' % i] = i, 'day'
			for i in range(15):
				Period['week_%d' % i] = i * 7, 'week'
			for i in range(12):
				Period['month_%d' % i] = i * 30, 'month'
			OneDay = day_1  # noqa  # pylint: disable=pointless-statement
			OneWeek = week_1  # noqa  # pylint: disable=pointless-statement

		self.assertFalse(hasattr(Period, '_ignore_'))
		self.assertFalse(hasattr(Period, 'Period'))
		self.assertFalse(hasattr(Period, 'i'))
		assert isinstance(Period.day_1, timedelta)

	def test_extend_enum_plain(self):

		class Color(UniqueEnum):
			red = 1
			green = 2
			blue = 3

		extend_enum(Color, 'brown', 4)
		assert Color.brown.name == 'brown'
		assert Color.brown.value == 4
		assert Color.brown in Color
		assert len(Color) == 4

	def test_extend_enum_shadow(self):

		class Color(UniqueEnum):
			red = 1
			green = 2
			blue = 3

		extend_enum(Color, 'value', 4)
		assert Color.value.name == 'value'
		assert Color.value.value == 4
		assert Color.value in Color
		assert len(Color) == 4
		assert Color.red.value == 1

	def test_extend_enum_unique_with_duplicate(self):
		with self.assertRaises(ValueError):

			class Color(Enum, settings=Unique):
				red = 1
				green = 2
				blue = 3

			extend_enum(Color, 'value', 1)

	def test_extend_enum_multivalue_with_duplicate(self):
		with self.assertRaises(ValueError):

			class Color(Enum, settings=MultiValue):
				red = 1, 'rojo'
				green = 2, 'verde'
				blue = 3, 'azul'

			extend_enum(Color, 'value', 2)

	def test_extend_enum_noalias_with_duplicate(self):

		class Color(Enum, settings=NoAlias):
			red = 1
			green = 2
			blue = 3

		extend_enum(
				Color,
				'value',
				3,
				)
		self.assertRaises(TypeError, Color, 3)
		assert Color.value is not Color.blue
		self.assertTrue(Color.value.value, 3)

	def test_no_duplicates(self):

		def bad_duplicates():

			class Color(UniqueEnum):
				red = 1
				green = 2
				blue = 3

			class Color(UniqueEnum):
				red = 1
				green = 2
				blue = 3
				grene = 2

		self.assertRaises(ValueError, bad_duplicates)

	def test_no_duplicates_kinda(self):

		class Silly(UniqueEnum):
			one = 1
			two = 'dos'
			name = 3

		class Sillier(IntEnum, UniqueEnum):
			single = 1
			name = 2
			triple = 3
			value = 4

	def test_auto_number(self):

		class Color(Enum, settings=AutoValue):
			red  # noqa  # pylint: disable=pointless-statement
			blue  # noqa  # pylint: disable=pointless-statement
			green  # noqa  # pylint: disable=pointless-statement

		assert list(Color), [Color.red, Color.blue == Color.green]
		assert Color.red.value == 1
		assert Color.blue.value == 2
		assert Color.green.value == 3

	def test_auto_name(self):

		class Color(Enum, settings=AutoValue):

			def _generate_next_value_(name, start, count, last):
				return name

			red  # noqa  # pylint: disable=pointless-statement
			blue  # noqa  # pylint: disable=pointless-statement
			green  # noqa  # pylint: disable=pointless-statement

		assert list(Color), [Color.red, Color.blue == Color.green]
		assert Color.red.value == 'red'
		assert Color.blue.value == 'blue'
		assert Color.green.value == 'green'

	def test_auto_name_inherit(self):

		class AutoNameEnum(Enum):

			def _generate_next_value_(name, start, count, last):
				return name

		class Color(AutoNameEnum, settings=AutoValue):
			red  # noqa  # pylint: disable=pointless-statement
			blue  # noqa  # pylint: disable=pointless-statement
			green  # noqa  # pylint: disable=pointless-statement

		assert list(Color), [Color.red, Color.blue == Color.green]
		assert Color.red.value == 'red'
		assert Color.blue.value == 'blue'
		assert Color.green.value == 'green'

	def test_auto_garbage(self):

		class Color(Enum):
			_settings_ = AutoValue
			red = 'red'
			blue  # noqa  # pylint: disable=pointless-statement

		assert Color.blue.value == 1

	def test_auto_garbage_corrected(self):

		class Color(Enum, settings=AutoValue):
			red = 'red'
			blue = 2
			green  # noqa  # pylint: disable=pointless-statement

		assert list(Color), [Color.red, Color.blue == Color.green]
		assert Color.red.value == 'red'
		assert Color.blue.value == 2
		assert Color.green.value == 3

	def test_duplicate_auto(self):

		class Dupes(Enum, settings=AutoValue):
			first = primero  # noqa  # pylint: disable=pointless-statement
			second  # noqa  # pylint: disable=pointless-statement
			third  # noqa  # pylint: disable=pointless-statement

		assert [Dupes.first, Dupes.second, Dupes.third] == list(Dupes)

	def test_order_as_function(self):
		# first with _init_
		class TestSequence(Enum):
			_init_ = 'value, sequence'
			_order_ = lambda member: member.sequence
			item_id = 'An$(1,6)', 0  # Item Code
			company_id = 'An$(7,2)', 1  # Company Code
			warehouse_no = 'An$(9,4)', 2  # Warehouse Number
			company = 'Hn$(13,6)', 3  # 4 SPACES + COMPANY
			key_type = 'Cn$(19,3)', 4  # Key Type = '1**'
			available = 'Zn$(1,1)', 5  # Available?
			contract_item = 'Bn(2,1)', 6  # Contract Item?
			sales_category = 'Fn', 7  # Sales Category
			gl_category = 'Rn$(5,1)', 8  # G/L Category
			warehouse_category = 'Sn$(6,1)', 9  # Warehouse Category
			inv_units = 'Qn$(7,2)', 10  # Inv Units

		for i, member in enumerate(TestSequence):
			assert i == member.sequence
		ts = TestSequence
		assert ts.item_id.name == 'item_id'
		assert ts.item_id.value == 'An$(1,6)'
		assert ts.item_id.sequence == 0
		assert ts.company_id.name == 'company_id'
		assert ts.company_id.value == 'An$(7,2)'
		assert ts.company_id.sequence == 1
		assert ts.warehouse_no.name == 'warehouse_no'
		assert ts.warehouse_no.value == 'An$(9,4)'
		assert ts.warehouse_no.sequence == 2
		assert ts.company.name == 'company'
		assert ts.company.value == 'Hn$(13,6)'
		assert ts.company.sequence == 3
		assert ts.key_type.name == 'key_type'
		assert ts.key_type.value == 'Cn$(19,3)'
		assert ts.key_type.sequence == 4
		assert ts.available.name == 'available'
		assert ts.available.value == 'Zn$(1,1)'
		assert ts.available.sequence == 5
		assert ts.contract_item.name == 'contract_item'
		assert ts.contract_item.value == 'Bn(2,1)'
		assert ts.contract_item.sequence == 6
		assert ts.sales_category.name == 'sales_category'
		assert ts.sales_category.value == 'Fn'
		assert ts.sales_category.sequence == 7
		assert ts.gl_category.name == 'gl_category'
		assert ts.gl_category.value == 'Rn$(5,1)'
		assert ts.gl_category.sequence == 8
		assert ts.warehouse_category.name == 'warehouse_category'
		assert ts.warehouse_category.value == 'Sn$(6,1)'
		assert ts.warehouse_category.sequence == 9
		assert ts.inv_units.name == 'inv_units'
		assert ts.inv_units.value == 'Qn$(7,2)'
		assert ts.inv_units.sequence == 10

		# and then without
		class TestSequence(Enum):
			_order_ = lambda member: member.value[1]
			item_id = 'An$(1,6)', 0  # Item Code
			company_id = 'An$(7,2)', 1  # Company Code
			warehouse_no = 'An$(9,4)', 2  # Warehouse Number
			company = 'Hn$(13,6)', 3  # 4 SPACES + COMPANY
			key_type = 'Cn$(19,3)', 4  # Key Type = '1**'
			available = 'Zn$(1,1)', 5  # Available?
			contract_item = 'Bn(2,1)', 6  # Contract Item?
			sales_category = 'Fn', 7  # Sales Category
			gl_category = 'Rn$(5,1)', 8  # G/L Category
			warehouse_category = 'Sn$(6,1)', 9  # Warehouse Category
			inv_units = 'Qn$(7,2)', 10  # Inv Units

		for i, member in enumerate(TestSequence):
			assert i == member.value[1]
		ts = TestSequence
		assert ts.item_id.name == 'item_id'
		assert ts.item_id.value, ('An$(1,6)' == 0)
		assert ts.company_id.name == 'company_id'
		assert ts.company_id.value, ('An$(7,2)' == 1)
		assert ts.warehouse_no.name == 'warehouse_no'
		assert ts.warehouse_no.value, ('An$(9,4)' == 2)
		assert ts.company.name == 'company'
		assert ts.company.value, ('Hn$(13,6)' == 3)
		assert ts.key_type.name == 'key_type'
		assert ts.key_type.value, ('Cn$(19,3)' == 4)
		assert ts.available.name == 'available'
		assert ts.available.value, ('Zn$(1,1)' == 5)
		assert ts.contract_item.name == 'contract_item'
		assert ts.contract_item.value, ('Bn(2,1)' == 6)
		assert ts.sales_category.name == 'sales_category'
		assert ts.sales_category.value, ('Fn' == 7)
		assert ts.gl_category.name == 'gl_category'
		assert ts.gl_category.value, ('Rn$(5,1)' == 8)
		assert ts.warehouse_category.name == 'warehouse_category'
		assert ts.warehouse_category.value, ('Sn$(6,1)' == 9)
		assert ts.inv_units.name == 'inv_units'
		assert ts.inv_units.value, ('Qn$(7,2)' == 10)
		# then with _init_ but without value
		with self.assertRaises(TypeError):

			class TestSequence(Enum):
				_init_ = 'sequence'
				_order_ = lambda member: member.sequence
				item_id = 'An$(1,6)', 0  # Item Code
				company_id = 'An$(7,2)', 1  # Company Code
				warehouse_no = 'An$(9,4)', 2  # Warehouse Number
				company = 'Hn$(13,6)', 3  # 4 SPACES + COMPANY
				key_type = 'Cn$(19,3)', 4  # Key Type = '1**'
				available = 'Zn$(1,1)', 5  # Available?
				contract_item = 'Bn(2,1)', 6  # Contract Item?
				sales_category = 'Fn', 7  # Sales Category
				gl_category = 'Rn$(5,1)', 8  # G/L Category
				warehouse_category = 'Sn$(6,1)', 9  # Warehouse Category
				inv_units = 'Qn$(7,2)', 10  # Inv Units

		# finally, out of order so Python 3 barfs
		with self.assertRaises(TypeError):

			class TestSequence(Enum):
				_init_ = 'sequence'
				_order_ = lambda member: member.sequence
				item_id = 'An$(1,6)', 0  # Item Code
				warehouse_no = 'An$(9,4)', 2  # Warehouse Number
				company = 'Hn$(13,6)', 3  # 4 SPACES + COMPANY
				company_id = 'An$(7,2)', 1  # Company Code
				inv_units = 'Qn$(7,2)', 10  # Inv Units
				available = 'Zn$(1,1)', 5  # Available?
				contract_item = 'Bn(2,1)', 6  # Contract Item?
				sales_category = 'Fn', 7  # Sales Category
				key_type = 'Cn$(19,3)', 4  # Key Type = '1**'
				gl_category = 'Rn$(5,1)', 8  # G/L Category
				warehouse_category = 'Sn$(6,1)', 9  # Warehouse Category

	def test_class_nested_enum_and_pickle_protocol_four(self):
		# would normally just have this directly in the class namespace
		class NestedEnum(Enum):
			twigs = 'common'
			shiny = 'rare'

		self.__class__.NestedEnum = NestedEnum
		self.NestedEnum.__qualname__ = '%s.NestedEnum' % self.__class__.__name__

	def test_subclasses_with_getnewargs_ex(self):

		class NamedInt(int):
			__qualname__ = 'NamedInt'  # needed for pickle protocol 4

			def __new__(cls, *args):
				_args = args
				if len(args) < 2:
					raise TypeError("name and value must be specified")
				name, args = args[0], args[1:]
				self = int.__new__(cls, *args)
				self._intname = name
				self._args = _args
				return self

			def __getnewargs_ex__(self):
				return self._args, {}

			@property
			def __name__(self):
				return self._intname

			def __repr__(self):
				# repr() is updated to include the name and type info
				return "{}({!r}, {})".format(type(self).__name__, self.__name__, int.__repr__(self))

			def __str__(self):
				# str() is unchanged, even if it relies on the repr() fallback
				base = int
				base_str = base.__str__
				if base_str.__objclass__ is object:
					return base.__repr__(self)
				return base_str(self)

			# for simplicity, we only define one operator that
			# propagates expressions
			def __add__(self, other):
				temp = int(self) + int(other)
				if isinstance(self, NamedInt) and isinstance(other, NamedInt):
					return NamedInt('({0} + {1})'.format(self.__name__, other.__name__), temp)
				else:
					return temp

		class NEI(NamedInt, Enum):
			__qualname__ = 'NEI'  # needed for pickle protocol 4
			x = ('the-x', 1)
			y = ('the-y', 2)

		assert NEI.__new__ is Enum.__new__
		assert repr(NEI.x + NEI.y), "NamedInt('(the-x + the-y)' == 3)"
		globals()['NamedInt'] = NamedInt
		globals()['NEI'] = NEI
		NI5 = NamedInt('test', 5)
		assert NI5 == 5
		assert NEI.y.value == 2


class MagicAutoNumberEnum(Enum, settings=AutoNumber):
	pass


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
