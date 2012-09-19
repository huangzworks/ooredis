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

    # encode

    def test_encode_with_JSONABLE(self):
        assert JsonTypeCase.encode(self.s) == json.dumps(self.s)

    def test_encode_RAISE_when_INPUT_UN_JSONABLE(self):
        with self.assertRaises(TypeError):
            JsonTypeCase.encode(self.wrong_type_input)

    # decode

    def test_decode_RETURN_NONE(self):
        assert JsonTypeCase.decode(None) == None

    def test_decode_RETURN_JSONABLE(self):
        assert JsonTypeCase.decode(json.dumps(self.s)) == self.s

    def test_decode_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            JsonTypeCase.decode(self.wrong_type_input)
