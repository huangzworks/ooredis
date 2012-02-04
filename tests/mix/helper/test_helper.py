#! /usr/bin/env python2.7
# coding:utf-8

import unittest

from ooredis.mix.key import Key
from ooredis.mix.helper import (
    get_key_name_from_list, 
    get_key_name_from_single_value,
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

if __name__ == "__main__":
    unittest.main()
