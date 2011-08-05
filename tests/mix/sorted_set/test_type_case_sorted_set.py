#! /usr/bin/env python2.7
# coding: utf-8

import unittest
import redis

from ooredis.client import connect

from ooredis.mix.key import Key
from ooredis.mix.sorted_set import SortedSet
from ooredis.type_case import JsonTypeCase

class TestTypeCaseSortedSet(unittest.TestCase):

    def setUp(self):
        connect()

        self.s = SortedSet('sorted_set', type_case=JsonTypeCase)

        self.value = 'hi'
        self.score = 1

        self.redispy = redis.Redis()
        self.redispy.flushdb()

    def tearDown(self):
        self.redispy.flushdb()

    def test_in(self):
        self.s[self.value] = self.score

        self.assertTrue(self.value in self.s)

    def test_setitem_and_getitem(self):
        self.s[self.value] = self.score

        self.assertEqual(self.s[0]['value'], self.value)
        self.assertEqual(self.s[0]['score'], self.score)

    def test_remove(self):
        self.s[self.value] = self.score

        self.s.remove(self.value)
        self.assertEqual(len(self.s), 0)

    def test_rank(self):
        self.s[self.value] = self.score

        self.assertEqual(self.s.rank(self.value), 0)
    
    def test_score(self):
        self.s[self.value] = self.score
        
        self.assertEqual(self.s.score(self.value), self.score)

    def test_incr(self):
        self.s[self.value] = self.score

        self.s.incr(self.value, 1)

        self.assertEqual(self.s.score(self.value), self.score+1)

    def test_decr(self):
        self.s[self.value] = self.score

        self.s.decr(self.value, 1)

        self.assertEqual(self.s.score(self.value), self.score-1)
if __name__ == "__main__":
    unittest.main()
