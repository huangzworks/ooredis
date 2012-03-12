#! /usr/bin/env python2.7
# coding: utf-8

import unittest
import redis

from ooredis.client import connect
from ooredis.mix.helper import format_key
from ooredis import String

class TestString(unittest.TestCase):

    def setUp(self):
        connect()

        self.redispy = redis.Redis()
        self.redispy.flushdb()
  
        self.name = 'name'
        self.value = 3.14

        self.key = String(self.name)

    def tearDown(self):
        self.redispy.flushdb()

    # __repr__

    def test_repr(self):
        self.key.set(self.value)

        self.assertEqual(repr(self.key),
                         format_key(self.key, self.name, self.value))

    # set

    def test_set(self): 
        self.key.set(self.value)
        self.assertEqual(self.key.get(), self.value)

    def test_set_with_expire(self):
        self.key.set(self.value, expire=3000)

        self.assertIsNotNone(self.key.ttl)
        self.assertEqual(self.key.get(), self.value)

    def test_set_preserve_with_exists_key(self):
        with self.assertRaises(ValueError):
            self.key.set('value')
            self.key.set('new_value', preserve=True) # overwrite false

    def test_set_preserve_with_not_exists_key(self):
        self.key.set('value', preserve=True)
        self.assertEqual(self.key.get(), 'value')

    def test_set_raises_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.lpush(self.key.name, 'list')
            self.key.set('value')

    # get

    def test_get_not_exists_key(self):
        self.assertIsNone(self.key.get())

    def test_get_exists_key(self):
        self.key.set(self.value)
        self.assertEqual(self.key.get(), self.value)

    def test_get_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.lpush(self.key.name, 'list')
            self.key.get()

    # getset

    def test_getset_return_NONE_cause_KEY_NOT_EXISTS(self):
        self.assertIsNone(self.key.getset(self.value))
        self.assertEqual(self.key.get(), self.value)

    def test_getset_return_OLD_VALUE_cause_KEY_EXISTS(self):
        self.new_value = 'new_value'
        self.old_value = self.value

        self.key.set(self.old_value)

        self.assertEqual(self.key.getset(self.new_value), self.old_value)
        self.assertEqual(self.key.get(), self.new_value)

    def test_getset_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.rpush(self.key.name, 'item')
            self.key.getset('value')

if __name__ == "__main__":
    unittest.main()
