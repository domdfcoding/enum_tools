#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  __init__.py
"""
Docstring Goes Here
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

__author__ = "Dominic Davis-Foster"
__copyright__ = "2020 Dominic Davis-Foster"

__license__ = "GNU Lesser General Public License v3 or later (LGPLv3+)"
__version__ = "0.0.1"
__email__ = "dominic@davis-foster.co.uk"

__all__ = [
		'constant',
		'Enum',
		'IntEnum',
		'AutoNumberEnum',
		'OrderedEnum',
		'UniqueEnum',
		'Flag',
		'IntFlag',
		'AutoNumber',
		'MultiValue',
		'NoAlias',
		'Unique',
		'unique',
		'NamedTuple',
		"EnumMeta",
		"__author__",
		"__copyright__",
		"__license__",
		"__version__",
		"__email__",
		]
# TODO: 'NamedConstant',
# TODO: 'skip',
# TODO: 'enum',
# TODO: 'extend_enum',

# this package
from ._constant import AutoNumber, AutoValue, MultiValue, NoAlias, Unique, constant
from .custom_enums import (
		AutoEnum,
		AutoNumberEnum,
		IntEnum,
		MultiValueEnum,
		NoAliasEnum,
		OrderedEnum,
		SqliteEnum,
		StrEnum,
		UniqueEnum
		)
from ._importer import Enum, EnumMeta, Flag, IntFlag, NamedTuple, unique
