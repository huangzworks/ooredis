#! /usr/bin/env python2.7
# coding: utf-8

import redis
import unittest

from ooredis import String
from ooredis.client import connect
from ooredis.key.helper import format_key

class TestString(unittest.TestCase):

    def setUp(self):
        connect()

        self.redispy = redis.Redis()
        self.redispy.flushdb()
  
        self.name = 'pi'
        self.value = 3.14

        self.key = String(self.name)

    def tearDown(self):
        self.redispy.flushdb()


    # __repr__

    def test_repr(self):
        self.key.set(self.value)

        self.assertEqual(
            repr(self.key),
            format_key(self.key, self.name, self.value)
        )
