#! /usr/bin/env python2.7
# coding: utf-8

import unittest
import redis

from ooredis.client import connect

from ooredis.mix.dict import Dict
from ooredis.type_case import JsonTypeCase

class TestTypeCaseDict(unittest.TestCase):
    
    def setUp(self):
        connect()
        self.d = Dict('dict', type_case=JsonTypeCase)

        self.redispy = redis.Redis()
        self.redispy.flushdb()

    def tearDown(self): 
        self.redispy.flushdb()

    def test_get_set(self):
        self.d['string'] = 'string'
        self.assertEqual(self.d['string'], 'string')

        self.d['int'] = 10086
        self.assertEqual(self.d['int'], 10086)

        self.d['float'] = 3.14
        self.assertEqual(self.d['float'], 3.14)

    def test_iter(self):
        self.d['string'] = 'string'
        self.d['int'] = 10086
        self.d['float'] = 3.14

        self.assertEqual(self.d.items(),
                         [('string', u'string'),
                          ('int', 10086),
                          ('float', 3.14)])
if __name__ == "__main__":
    unittest.main()
