#! /usr/bin/env python2.7
# coding: utf-8

import unittest
import redis

from ooredis.client import connect

from ooredis.mix.set import Set
from ooredis.type_case import JsonTypeCase

class TestTypeCaseSet(unittest.TestCase):
    
    def setUp(self):
        connect()

        self.s = Set('set', type_case=JsonTypeCase)
        self.another = Set('another', type_case=JsonTypeCase)

        self.data = {'value': 3.14}

        self.redispy = redis.Redis()
        self.redispy.flushdb()

    def tearDown(self):
        self.redispy.flushdb()

    # len
    # add

    def test_add_len(self):
        self.assertEqual(len(self.s), 0)

        self.s.add('e')
        self.assertEqual(len(self.s), 1)

    def test_len_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set('set', 'string')
            len(self.s)

        self.data = {'value': 3.14}

        self.redispy = redis.Redis()
        self.redispy.flushdb()

    def tearDown(self):
        self.redispy.flushdb()

    def test_add_and_pop(self):
        self.s.add(self.data)

        self.assertEqual(self.s.pop(), self.data)

    def test_random(self):
        self.s.add(self.data)

        self.assertEqual(self.s.random(), self.data)

    def test_iter(self):
        self.s.add(self.data)

        self.assertEqual(list(self.s), [self.data])

    def test_in(self):
        self.s.add(self.data)

        self.assertTrue(self.data in self.s)

    def test_delete(self):
        self.s.add(self.data)

        self.s.remove(self.data)
        self.assertEqual(len(self.s), 0)

    def test_move(self):
        self.s.add(self.data)

        self.s.move(self.another, self.data)

        self.assertEqual(self.another.pop(), self.data)

    def test_and(self):
        self.data = "10086"

        self.s.add(self.data)
        self.another.add(self.data)

        self.assertEqual(self.s & self.another, {self.data})
        
if __name__ == "__main__":
    unittest.main()
