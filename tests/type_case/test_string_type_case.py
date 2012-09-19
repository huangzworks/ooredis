# coding: utf-8

from unittest import TestCase
from ooredis.type_case import StringTypeCase

class TestString(TestCase):

    def setUp(self):
        self.s = 'str'
        self.u = u'unicode'

        self.wrong_type_input = set()

    # encode

    def test_encode_ACCEPT_STR(self):
        assert StringTypeCase.encode(self.s) == self.s

    def test_encode_ACCEPT_UNICODE(self):
        assert StringTypeCase.encode(self.u) == self.u

    def test_encode_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            StringTypeCase.encode(self.wrong_type_input)

    # decode

    def test_decode_RETURN_NONE(self):
        assert StringTypeCase.decode(None) == None

    def test_decode_RETURN_STR(self):
        assert StringTypeCase.decode(self.s) == self.s

    def test_decode_RETURN_UNICODE(self):
        assert StringTypeCase.decode(self.u) == self.u
