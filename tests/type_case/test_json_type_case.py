# coding: utf-8

import json

from unittest import TestCase
from ooredis.type_case import JsonTypeCase

class UnJsonableObj:
    pass

class TestJson(TestCase):

    def setUp(self):
        self.s = 'str'

        self.wrong_type_input = UnJsonableObj()

    # to_redis

    def test_to_redis_with_JSONABLE(self):
        assert JsonTypeCase.to_redis(self.s) == json.dumps(self.s)

    def test_to_redis_RAISE_when_INPUT_UN_JSONABLE(self):
        with self.assertRaises(TypeError):
            JsonTypeCase.to_redis(self.wrong_type_input)

    # to_python

    def test_to_python_RETURN_NONE(self):
        assert JsonTypeCase.to_python(None) == None

    def test_to_python_RETURN_JSONABLE(self):
        assert JsonTypeCase.to_python(json.dumps(self.s)) == self.s

    def test_to_python_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            JsonTypeCase.to_python(self.wrong_type_input)
