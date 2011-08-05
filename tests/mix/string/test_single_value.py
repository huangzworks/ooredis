#! /usr/bin/env python2.7
# coding: utf-8

import unittest
import redis

from ooredis.client import connect
from ooredis.mix.string import SingleValue

class TestMutableMix(unittest.TestCase):

    def setUp(self):
        connect()

        self.redispy = redis.Redis()
        self.redispy.flushdb()
   
        self.key = SingleValue('string')
        self.value = 3.14

    def tearDown(self):
        self.redispy.flushdb()

    # __repr__

    def test_repr(self):
        self.assertIsNotNone(repr(self))

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
        assert(self.key.exists == False) 

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

    def test_getset_with_not_exists_key(self):
        # 没有预设值，返回None。
        assert(self.key.exists == False)
        self.assertIsNone(self.key.getset(self.value))
        self.assertEqual(self.key.get(), self.value)

    def test_getset_with_exists_key(self):
        self.key.set(self.value)
        # 有预设值，返回预设值。
        self.assertEqual(self.key.getset('new'), self.value)
        self.assertEqual(self.key.get(), 'new')

    def test_getset_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.rpush(self.key.name, 'item')
            self.key.getset('value')

if __name__ == "__main__":
    unittest.main()
