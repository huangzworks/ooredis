# coding: utf-8

from unittest import TestCase
from ooredis.type_case.helper import *

class TestHelper(TestCase):

    def setUp(self):    
        self.s = 'string'

    def test_is_any_instance_TRUE(self):
        assert is_any_instance(self.s, str)

    def test_is_any_instance_FALSE(self):
        assert not is_any_instance(self.s, float)

    def test_is_any_instance_TRUE_in_GIVEN_MULTI_TYPES(self):
        assert is_any_instance(self.s, str, float)
        assert is_any_instance(self.s, int, str, float)

    def test_is_any_instance_FALSE_in_GIVEN_MULTI_TYPES(self):
        assert not is_any_instance(self.s, float, int, list)
        assert not is_any_instance(self.s, set, int, float)
