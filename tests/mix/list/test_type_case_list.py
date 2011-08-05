#! /usr/bin/env python2.7
# coding: utf-8

import unittest
import redis

from ooredis.client import connect
from ooredis.mix.list import List
from ooredis.type_case import JsonTypeCase

class TestTypeCaseList(unittest.TestCase):
    
    def setUp(self):
        connect()
        self.l = List('list', type_case=JsonTypeCase)
        self.destination = List('destination',
                                type_case=JsonTypeCase)

        self.data = {'value': 3.14}

        self.redispy = redis.Redis()
        self.redispy.flushdb()

    def tearDown(self):
        self.redispy.flushdb()

    def test_setitem_and_getitem(self):
        self.l.rpush('holder')

        self.l[0] = self.data
        self.assertEqual(self.l[0], self.data)

        # range
        self.assertEqual(self.l[:], [self.data])

    def test_rpush_and_rpop(self):
        self.l.rpush(self.data)
        self.assertEqual(self.l.rpop(), self.data)

    def test_lpush_and_lpop(self):
        self.l.lpush(self.data)
        self.assertEqual(self.l.lpop(), self.data)

    def test_blpop(self):
        self.l.lpush(self.data)
        self.assertEqual(self.l.blpop(), self.data)

    def test_brpop(self):
        self.l.lpush(self.data)
        self.assertEqual(self.l.brpop(), self.data)

    def test_rpoplpush(self):
        self.l.lpush(self.data)
        self.assertEqual(
            self.l.rpoplpush(self.destination),
            self.data)
    
        self.assertEqual(self.destination.lpop(), self.data)

    def test_brpoplpush(self):
        self.l.lpush(self.data)
        self.assertEqual(
            self.l.brpoplpush(self.destination),
            self.data)

        self.assertEqual(self.destination.lpop(), self.data)

    def test_in(self):
        self.l.lpush(self.data)

        self.assertTrue(self.data in self.l)

    # remove

    def test_remove(self):
        self.l.lpush(self.data)

        self.l.remove(self.data)
        self.assertEqual(len(self.l), 0)

if __name__ == "__main__":
    unittest.main()
