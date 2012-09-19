# coding: utf-8

from unittest import TestCase
from ooredis.type_case import IntTypeCase

class TestInt(TestCase):

    def setUp(self):
        self.i = 10086
        self.l = 100861008610086

        self.wrong_type_input = set()

    # encode

    def test_encode_ACCEPT_INT(self):
        assert IntTypeCase.encode(self.i) == self.i

    def test_encode_ACCEPT_LONG(self):
        assert IntTypeCase.encode(self.l) == self.l

    def test_encode_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            IntTypeCase.encode(self.wrong_type_input)

    # decode

    def test_decode_RETURN_NONE(self):
        assert IntTypeCase.decode(None) == None

    def test_decode_RETURN_INT(self):    
        assert IntTypeCase.decode(str(self.i)) == self.i

    def test_decode_RETURN_LONG(self):
        assert IntTypeCase.decode(str(self.l)) == self.l

    def test_decode_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            IntTypeCase.decode(self.wrong_type_input)
