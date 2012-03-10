# coding: utf-8

from unittest import TestCase
from ooredis.type_case import IntTypeCase

class TestInt(TestCase):

    def setUp(self):
        self.i = 10086
        self.l = 100861008610086

        self.wrong_type_input = set()

    # to_redis

    def test_to_redis_ACCEPT_INT(self):
        assert IntTypeCase.to_redis(self.i) == self.i

    def test_to_redis_ACCEPT_LONG(self):
        assert IntTypeCase.to_redis(self.l) == self.l

    def test_to_redis_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            IntTypeCase.to_redis(self.wrong_type_input)

    # to_python

    def test_to_python_RETURN_NONE(self):
        assert IntTypeCase.to_python(None) == None

    def test_to_python_RETURN_INT(self):    
        assert IntTypeCase.to_python(str(self.i)) == self.i

    def test_to_python_RETURN_LONG(self):
        assert IntTypeCase.to_python(str(self.l)) == self.l

    def test_to_python_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            IntTypeCase.to_python(self.wrong_type_input)
