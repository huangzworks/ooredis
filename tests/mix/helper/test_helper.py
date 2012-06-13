#! /usr/bin/env python2.7
# coding:utf-8

import unittest
import redis

from ooredis.mix.key import Key
from ooredis.mix.helper import (
    get_key_name_from_list, 
    get_key_name_from_single_value,
    format_key,
    catch_wrong_type_error,
)

class TestHelper(unittest.TestCase):

    def setUp(self):
        self.name = "name"
        self.value = "value"
        self.key = Key(self.name)

    # get_key_name_from_single_value

    def test_get_key_name_from_single_value_with_key_object(self):
        self.assertEqual(
            get_key_name_from_single_value(self.key),
            self.key.name)

    def test_get_key_name_from_single_value_with_key_name(self):
        self.assertEqual(
            get_key_name_from_single_value(self.key.name),
            self.key.name)

    # get_key_name_from_list

    def test_get_key_name_from_list_with_key_objects(self):
        self.assertListEqual(
            get_key_name_from_list([self.key]),
            [self.key.name])

    def test_get_key_name_from_list_with_key_names(self):
        self.assertListEqual(
            get_key_name_from_list([self.key.name]),
            [self.key.name])

    # format_key

    def test_format_key(self):
        output = format_key(self.key, self.name, self.value)
        self.assertEqual( output,"Key Key 'name': value")

    
    # catch_wrong_type_error

    def test_catch_wrong_type_error_RAISE_TYPE_ERROR_when_ERROR_OCCUR(self):

        @catch_wrong_type_error
        def r():
            raise redis.exceptions.ResponseError

        with self.assertRaises(TypeError):
            r() 

    def test_catch_wrong_type_error_NOT_RAISE_when_NO_ERROR_OCCUR(self):

        @catch_wrong_type_error
        def f():
            return 10

        self.assertEqual(
            f(),
            10
        )

if __name__ == "__main__":
    unittest.main()
