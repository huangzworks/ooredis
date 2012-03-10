# coding: utf-8

from unittest import TestCase
from ooredis.type_case import StringTypeCase

class TestString(TestCase):

    def setUp(self):
        self.s = 'str'
        self.u = u'unicode'

        self.wrong_type_input = set()

    # to_redis

    def test_to_redis_ACCEPT_STR(self):
        assert StringTypeCase.to_redis(self.s) == self.s

    def test_to_redis_ACCEPT_UNICODE(self):
        assert StringTypeCase.to_redis(self.u) == self.u

    def test_to_redis_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            StringTypeCase.to_redis(self.wrong_type_input)

    # to_python

    def test_to_python_RETURN_NONE(self):
        assert StringTypeCase.to_python(None) == None

    def test_to_python_RETURN_STR(self):
        assert StringTypeCase.to_python(self.s) == self.s

    def test_to_python_RETURN_UNICODE(self):
        assert StringTypeCase.to_python(self.u) == self.u
