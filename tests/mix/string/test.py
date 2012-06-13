#! /usr/bin/env python2.7
# coding: utf-8

import unittest
import redis

from ooredis import String
from ooredis.client import connect
from ooredis.mix.helper import format_key
from ooredis.type_case import FloatTypeCase

class TestString(unittest.TestCase):

    def setUp(self):
        connect()

        self.redispy = redis.Redis()
        self.redispy.flushdb()
  
        self.name = 'pi'
        self.value = 3.14

        self.key = String(self.name, type_case=FloatTypeCase)

    def tearDown(self):
        self.redispy.flushdb()

    def set_wrong_type(self):
        self.redispy.lpush(self.name, "create a list value")


    # __repr__

    def test_repr(self):
        self.key.set(self.value)

        self.assertEqual(
            repr(self.key),
            format_key(self.key, self.name, self.value)
        )


    # set

    def test_set(self): 
        self.key.set(self.value)

        self.assertEqual(
            self.key.get(),
            self.value
        )

    def test_set_with_EXPIRE(self):
        self.key.set(self.value, expire=3000)

        self.assertIsNotNone(
            self.key.ttl
        )
        self.assertEqual(
            self.key.get(),
            self.value
        )

    def test_set_preserve_with_exists_key(self):
        with self.assertRaises(ValueError):
            self.key.set(self.value)
            self.key.set(self.value, preserve=True) # overwrite false

    def test_set_preserve_with_not_exists_key(self):
        self.key.set(self.value, preserve=True)
        self.assertEqual(self.key.get(), self.value)

    def test_set_raises_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.lpush(self.key.name, 'list')
            self.key.set('value')

    
    # setnx

    def test_setnx_with_NO_EXISTS_KEY(self):
        self.key.setnx(self.value)

        self.assertEqual(
            self.key.get(),
            self.value
        )

    def test_setnx_with_EXISTS_KEY(self):
        self.key.setnx(self.value)

        self.key.setnx(10086)   # this value will not set

        self.assertEqual(
            self.key.get(),
            self.value
        )

    def test_setnx_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type()
            self.key.setnx(self.value)

    
    # setex

    def test_setex_with_NO_EXISTS_KEY(self):
        self.key.setex(self.value, 10086)

        self.assertIsNotNone(
            self.key.ttl
        )

        self.assertEqual(
            self.key.get(),
            self.value
        )

    def test_setex_with_EXISTS_KEY(self):
        self.key.setex(self.value, 10086)

        self.key.setex(self.value, 100)

        self.assertTrue(
            self.key.ttl <= 100
        )

        self.assertEqual(
            self.key.get(),
            self.value
        )

    def test_setex_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type()
            self.key.setex(self.value, 10086)


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
        self.new_value = 10086
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
