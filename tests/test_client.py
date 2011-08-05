#! /usr/bin/env python2.7
# coding:utf-8

import unittest

from ooredis.client import connect, get_client
import redis

class TestClient(unittest.TestCase):
    
    def setUp(self):
        self.client = connect()

    def test_get(self):
        self.assertTrue(isinstance(get_client(), redis.Redis))

    def test_get_get(self):
        self.assertEqual(get_client(), get_client())

if __name__ == "__main__":
    unittest.main()
