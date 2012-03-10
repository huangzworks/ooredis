# coding: utf-8

from unittest import TestCase
from ooredis.type_case import GenericTypeCase

class TestGeneric(TestCase):

    def setUp(self):
        self.s = 'str'
        self.u = u'unicode'
        self.i = 10086
        self.l = 100861008610086
        self.f = 3.14

        self.wrong_type_input = set()

    # to_redis

    def test_to_redis_ACCEPT_STRING(self):
        assert GenericTypeCase.to_redis(self.s) == self.s
    
    def test_to_redis_ACCEPT_UNICODE(self):
        assert GenericTypeCase.to_redis(self.u) == self.u

    def test_to_redis_ACCEPT_INT(self):
        assert GenericTypeCase.to_redis(self.i) == self.i

    def test_to_redis_ACCEPT_LONG(self):
        assert GenericTypeCase.to_redis(self.l) == self.l

    def test_to_redis_ACCEPT_FLOAT(self):
        assert GenericTypeCase.to_redis(self.f) == self.f

    def test_to_redis_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            GenericTypeCase.to_redis(self.wrong_type_input)

    # to_python

    def test_to_python_RETURN_NONE(self):
        assert GenericTypeCase.to_python(None) is None

    def test_to_python_RETURN_STRING(self):
        assert GenericTypeCase.to_python(str(self.s)) == self.s

    def test_to_python_RETURN_UNICODE(self):
        assert GenericTypeCase.to_python(unicode(self.u)) == self.u

    def test_to_python_RETURN_INT(self):
        assert GenericTypeCase.to_python(str(self.i)) == self.i

    def test_to_python_RETURN_LONG(self):
        assert GenericTypeCase.to_python(str(self.l)) == self.l

    def test_to_python_RETURN_FLOAT(self):
        assert GenericTypeCase.to_python(str(self.f)) == self.f

    def test_to_python_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            GenericTypeCase.to_python(self.l)
