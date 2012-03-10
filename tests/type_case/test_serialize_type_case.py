# coding: utf-8

import pickle

from unittest import TestCase
from ooredis.type_case import SerializeTypeCase

class SerializeAbleClass:
    greet = 'hello moto'

class TestSerializeTypeCase(TestCase):

    def setUp(self):
        self.s = 'str'
        self.c = SerializeAbleClass()

    # to_redis

    def test_to_redis_with_STR(self):
        assert SerializeTypeCase.to_redis(self.s) == pickle.dumps(self.s)

    def test_to_redis_with_CLASS(self):
        assert SerializeTypeCase.to_redis(self.c) == pickle.dumps(self.c)

    # to_python

    def test_to_python_RETURN_NONE(self):
        assert SerializeTypeCase.to_python(None) == None

    def test_to_python_RETURN_STR(self):
        assert SerializeTypeCase.to_python(SerializeTypeCase.to_redis(self.s)) == self.s

    def test_to_python_RETURN_CLASS(self):
        assert isinstance(SerializeTypeCase.to_python(SerializeTypeCase.to_redis(self.c)), SerializeAbleClass)
