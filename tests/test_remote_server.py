#! /usr/bin/env python2.7
# coding:utf-8

import unittest

from ooredis import connect, get_client, SingleValue
import redis

class TestRemoteServer(unittest.TestCase):
    
    def setUp(self):
        self.host = '127.0.0.1'

        # ooredis
        connect(host=self.host)
       
        # redis-py
        self.r = redis.Redis(host=self.host)
        self.r.flushdb()

    def test_set_and_get(self):
        self.s = SingleValue('key')
        self.s.set('value')

        self.assertEqual(self.s.get(), 'value')

        self.assertTrue(self.r.exists('key'))
        self.assertEqual(self.r.get('key'), self.s.get())

if __name__ == "__main__":
    unittest.main()
