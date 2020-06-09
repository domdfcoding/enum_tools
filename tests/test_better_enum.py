# -*- coding: utf-8 -*-

# stdlib
from unittest import TestCase


class TestStarImport(TestCase):

	def test_all_exports_names(self):
		scope = {}
		exec('from better_enum import *', scope, scope)
		self.assertIn('Enum', scope)
