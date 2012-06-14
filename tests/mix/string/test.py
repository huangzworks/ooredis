#! /usr/bin/env python2.7
# coding: utf-8

import redis
import unittest

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

        # 使用 FloatTypeCase 是为了测试 TypeCase
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

    def test_set_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type()
            self.key.set(self.value)

    
    # setnx

    def test_setnx_with_NO_EXISTS_KEY(self):
        self.key.setnx(self.value)

        self.assertEqual(
            self.key.get(),
            self.value
        )

    def test_setnx_WILL_NOT_OVERWRITE_EXISTS_VALUE(self):
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

    def test_setex_WILL_UPDATE_EXPIRE_TIME_when_KEY_EXISTS(self):
        self.key.setex(self.value, 10086)

        self.key.setex(self.value, 100)     # overwrite 10086 (origin ttl)

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

    def test_get_RETURN_NONE_when_KEY_NOT_EXISTS(self):
        self.assertIsNone(
            self.key.get()
        )

    def test_get_with_EXISTS_KEY(self):
        self.key.set(self.value)

        self.assertEqual(
            self.key.get(), 
            self.value
        )

    def test_get_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type()
            self.key.get()


    # getset

    def test_getset_RETURN_NONE_when_KEY_NOT_EXISTS(self):
        self.assertIsNone(
            self.key.getset(self.value)
        )

        self.assertEqual(
            self.key.get(),
            self.value
        )

    def test_getset_RETURN_OLD_VALUE_when_KEY_EXISTS(self):
        self.new_value = 10086
        self.old_value = self.value

        self.key.set(self.old_value)

        self.assertEqual(
            self.key.getset(self.new_value),
            self.old_value
        )

        self.assertEqual(
            self.key.get(), 
            self.new_value
        )

    def test_getset_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type()
            self.key.getset('value')


if __name__ == "__main__":
    unittest.main()
