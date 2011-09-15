#! /usr/bin/env python2
# coding: utf-8

import unittest
from ooredis import Server
from redis import Redis

class TestServer(unittest.TestCase):
    
    def setUp(self):
        self.r = Redis()

    """
    flushdb
    """

    def test_flushdb_with_empty_db(self):
        self.r.flushdb()    # flush
        self.assertEqual(self.r.keys('*'), [])

        Server.flushdb()    # flush again
        self.assertEqual(self.r.keys('*'), [])

    def test_flushdb_with_not_empty_db(self):
        self.r.set('key', 'value')
        self.assertNotEqual(self.r.keys('*'), [])

        Server.flushdb()
        self.assertEqual(self.r.keys('*'), [])
