# coding: utf-8

from unittest import TestCase
from ooredis.type_case import FloatTypeCase

class TestFloat(TestCase):

    def setUp(self):
        self.f = 3.14
        self.i = 10086

        self.wrong_type_input = set()

    # to_redis

    def test_to_redis_ACCEPT_FLOAT(self):
        assert FloatTypeCase.to_redis(self.f) == self.f

    def test_to_redis_ACCEPT_INT(self):
        assert FloatTypeCase.to_redis(self.i) == float(self.i)

    def test_to_redis_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            FloatTypeCase.to_redis(self.wrong_type_input)

    # to_python

    def test_to_python_RETURN_NONE(self):
        assert FloatTypeCase.to_python(None) == None

    def test_to_python_RETURN_FLOAT(self):
        assert FloatTypeCase.to_python(str(self.f)) == self.f

    def test_to_python_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            FloatTypeCase.to_python(self.wrong_type_input)
