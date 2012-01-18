#! /usr/bin/env python2.7
# coding: utf-8

import unittest
import redis

from ooredis.client import connect
from ooredis.mix.single_value import Counter

class TestCounter(unittest.TestCase):
    
    def setUp(self):
        connect()

        self.redispy = redis.Redis()
        self.redispy.flushdb()

        self.counter = Counter('counter')

    def tearDown(self):
        self.redispy.flushdb()
        
    # incr

    def test_incr(self):
        self.assertEqual(self.counter.incr(), 1)

    def test_incr_with_increment(self):
        self.assertEqual(self.counter.incr(2), 2)

    def test_incr_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.counter.name, 'string')
            self.counter.incr()

    # decr

    def test_decr(self):
        self.assertEqual(self.counter.decr(), -1)

    def test_decr(self):
        self.assertEqual(self.counter.decr(2), -2)

    def test_decr_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.counter.name, 'string')
            self.counter.decr()

    def test_decr(self):
        self.assertEqual(self.counter.decr(), -1)

    def test_decr(self):
        self.assertEqual(self.counter.decr(2), -2)

    # iadd

    def test_iadd(self):
        self.counter += 1
        self.assertEqual(self.counter.get(), 1)

    def test_iadd_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.counter.name, 'string')
            self.counter += 1

    # isub

    def test_isub(self):
        self.counter -= 1
        self.assertEqual(self.counter.get(), -1)

    def test_isub_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.counter.name, 'string')
            self.counter -= 1

    # get
    def test_get(self):
        self.assertIsNone(self.counter.get())

        self.counter += 1
        self.assertEqual(self.counter.get(), 1)

    # set

    def test_set(self):
        self.counter.set(10086)

        self.assertEqual(self.counter.get(), 10086)
        
        self.counter += 1
        self.assertEqual(self.counter.get(), 10087)

    # getset

    def test_getset(self):
        self.assertIsNone(self.counter.getset(10086))

        self.assertEqual(10086, self.counter.getset(1))
        
        self.assertEqual(self.counter.get(), 1)

if __name__ == "__main__":
    unittest.main()
