#! /usr/bin/env python2.7
# coding:utf-8

import redis
import unittest

from ooredis.key.base_key import BaseKey
from ooredis.const import REDIS_TYPE
from ooredis.type_case import GenericTypeCase
from ooredis.client import connect, get_client

class TestBaseKey(unittest.TestCase):
    
    def setUp(self):
        connect()
    
        self.name = "name"
        self.value = "value"

        self.key = BaseKey(self.name)

        self.redispy = redis.Redis()
        self.redispy.flushdb()

    def tearDown(self):
        self.redispy.flushdb()


    # __init__

    def test_init_key(self):
        self.assertTrue(
            isinstance(self.key._client, redis.Redis)
        )

        self.assertEqual(
            get_client(),
            self.key._client
        )

        self.assertEqual(
            self.key.encode,
            GenericTypeCase.encode
        )
        self.assertEqual(
            self.key.decode,
            GenericTypeCase.decode
        )


    # __eq__

    def test__eq__TRUE(self):
        self.assertEqual(
            self.key, 
            BaseKey(self.name)
        )

    def test__eq__FALSE(self):
        self.assertNotEqual(
            self.key,
            BaseKey('another-key')
        )

if __name__ == "__main__":
    unittest.main()
