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

    # encode

    def test_encode_with_STR(self):
        assert SerializeTypeCase.encode(self.s) == pickle.dumps(self.s)

    def test_encode_with_CLASS(self):
        assert SerializeTypeCase.encode(self.c) == pickle.dumps(self.c)

    # decode

    def test_decode_RETURN_NONE(self):
        assert SerializeTypeCase.decode(None) == None

    def test_decode_RETURN_STR(self):
        assert SerializeTypeCase.decode(SerializeTypeCase.encode(self.s)) == self.s

    def test_decode_RETURN_CLASS(self):
        assert isinstance(SerializeTypeCase.decode(SerializeTypeCase.encode(self.c)), SerializeAbleClass)
