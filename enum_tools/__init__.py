#!/usr/bin/env python3
#
#  __init__.py
"""
Tools to expand Python's enum module.
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

# stdlib
from enum import Enum, Flag, IntFlag

# this package
from enum_tools.custom_enums import AutoNumberEnum, DuplicateFreeEnum, IntEnum, OrderedEnum, StrEnum
from enum_tools.documentation import DocumentedEnum, document_enum, document_member

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "GNU Lesser General Public License v3 or later (LGPLv3+)"
__version__: str = "0.8.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = [
		"Enum",
		"IntEnum",
		"StrEnum",
		"AutoNumberEnum",
		"OrderedEnum",
		"DuplicateFreeEnum",
		"Flag",
		"IntFlag",
		"DocumentedEnum",
		"document_enum",
		"document_member",
		]
