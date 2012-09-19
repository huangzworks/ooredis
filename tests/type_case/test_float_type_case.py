# coding: utf-8

from unittest import TestCase
from ooredis.type_case import FloatTypeCase

class TestFloat(TestCase):

    def setUp(self):
        self.f = 3.14
        self.i = 10086

        self.wrong_type_input = set()

    # encode

    def test_encode_ACCEPT_FLOAT(self):
        assert FloatTypeCase.encode(self.f) == self.f

    def test_encode_ACCEPT_INT(self):
        assert FloatTypeCase.encode(self.i) == float(self.i)

    def test_encode_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            FloatTypeCase.encode(self.wrong_type_input)

    # decode

    def test_decode_RETURN_NONE(self):
        assert FloatTypeCase.decode(None) == None

    def test_decode_RETURN_FLOAT(self):
        assert FloatTypeCase.decode(str(self.f)) == self.f

    def test_decode_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            FloatTypeCase.decode(self.wrong_type_input)
