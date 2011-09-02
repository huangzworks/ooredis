#! /usr/bin/env python2.7
# coding: utf-8

import unittest
import redis

from ooredis.client import connect
from ooredis.mix.single_value import SingleValue
from ooredis.type_case import SerializeTypeCase

class Person:
    name = 'huangz'

class TestTypeCaseSingleValue(unittest.TestCase):

    def setUp(self):
        connect()

        self.redispy = redis.Redis()
        self.redispy.flushdb()
   
        self.key = SingleValue('object', type_case=SerializeTypeCase)
        self.obj = Person()

    def tearDown(self):
        self.redispy.flushdb()

    def test_get_and_set(self):
        self.key.set(self.obj)

        self.assertTrue(isinstance(self.key.get(), Person))
        self.assertEqual(self.key.get().name, self.obj.name)

    def test_getset(self):
        self.assertIsNone(self.key.getset(self.obj))

        self.assertTrue(isinstance(self.key.get(), Person))
        self.assertEqual(self.key.get().name, self.obj.name)

if __name__ == "__main__":
    unittest.main()