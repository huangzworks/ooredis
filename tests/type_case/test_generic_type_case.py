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

    # encode

    def test_encode_ACCEPT_STRING(self):
        assert GenericTypeCase.encode(self.s) == self.s
    
    def test_encode_ACCEPT_UNICODE(self):
        assert GenericTypeCase.encode(self.u) == self.u

    def test_encode_ACCEPT_INT(self):
        assert GenericTypeCase.encode(self.i) == self.i

    def test_encode_ACCEPT_LONG(self):
        assert GenericTypeCase.encode(self.l) == self.l

    def test_encode_ACCEPT_FLOAT(self):
        assert GenericTypeCase.encode(self.f) == self.f

    def test_encode_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            GenericTypeCase.encode(self.wrong_type_input)

    # decode

    def test_decode_RETURN_NONE(self):
        assert GenericTypeCase.decode(None) is None

    def test_decode_RETURN_STRING(self):
        assert GenericTypeCase.decode(str(self.s)) == self.s

    def test_decode_RETURN_UNICODE(self):
        assert GenericTypeCase.decode(unicode(self.u)) == self.u

    def test_decode_RETURN_INT(self):
        assert GenericTypeCase.decode(str(self.i)) == self.i

    def test_decode_RETURN_LONG(self):
        assert GenericTypeCase.decode(str(self.l)) == self.l

    def test_decode_RETURN_FLOAT(self):
        assert GenericTypeCase.decode(str(self.f)) == self.f

    def test_decode_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(AssertionError):
            GenericTypeCase.decode(self.l)
