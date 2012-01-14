#! /usr/bin/env python2.7
# coding:utf-8

import unittest
import redis
import numbers

from ooredis.client import connect, get_client
from ooredis.mix.key import Key
from ooredis.mix.key import (
    get_key_name_from_list, 
    get_key_name_from_single_value,
)
from ooredis.const import REDIS_TYPE
from ooredis.type_case import GenericTypeCase

class TestKey(unittest.TestCase):
    
    def setUp(self):
        connect()
    
        self.name = "name"
        self.value = "value"
        self.key = Key(self.name)

        self.redispy = redis.Redis()
        self.redispy.flushdb()

    def tearDown(self):
        self.redispy.flushdb()

    # __init__

    def test_key_client(self):
        self.assertTrue(isinstance(self.key._client, redis.Redis))

        self.assertEqual(get_client(), self.key._client)

        self.assertEqual(self.key._type_case, GenericTypeCase)

    # __eq__

    def test_key_equal(self):
        # equal
        self.assertEqual(self.key, Key(self.name))

        # not equal
        self.assertNotEqual(self.key, Key('hahaha'))

    # __str__

    def test_str(self):
        self.assertEqual(str(self.key), "<{0} Key '{1}'>".format(self.key.__class__.__name__.title(), self.key.name))

    # _name

    def test_cant_change_key_name(self):
        with self.assertRaises(AttributeError):
            self.key.name = 'new_name'

    # _represent

    def test_represent(self):
        # string
        self.redispy.set('string', 'string')
        self.assertEqual(Key('string')._represent,
                         REDIS_TYPE['string'])

        # list
        self.redispy.lpush('list', 'itme')
        self.assertEqual(Key('list')._represent,
                         REDIS_TYPE['list'])

        # set
        self.redispy.sadd('set', 'element')
        self.assertEqual(Key('set')._represent,
                         REDIS_TYPE['set'])

        # sorted set
        self.redispy.zadd('sorted_set', 'value', 30)
        self.assertEqual(Key('sorted_set')._represent,
                         REDIS_TYPE['sorted_set'])

        # hash
        self.redispy.hset('hash', 'field', 'value')
        self.assertEqual(Key('hash')._represent,
                         REDIS_TYPE['hash'])

        # not exists key
        self.assertFalse(self.redispy.exists('not_exists_key'))
        self.assertEqual(Key('not_exists_key')._represent,
                         REDIS_TYPE['not_exists'])

    # ttl

    def test_ttl(self):
        # 无TTL的key
        self.redispy.set(self.key.name, self.value)
        self.assertIsNone(self.key.ttl)

        # 带ttl的key
        self.redispy.expire(self.key.name, 300)
        self.assertIsNotNone(self.key.ttl)
        self.assertTrue(isinstance(self.key.ttl, numbers.Number))

        # 不存在或过期的key
        self.redispy.delete(self.key.name)
        self.assertIsNone(self.key.ttl)

    # exists

    def test_exists(self):
        # 不存在
        self.assertFalse(self.key.exists)

        # 存在
        self.redispy.set(self.key.name, self.value)
        self.assertTrue(self.key.exists)

    # delete

    def test_delete(self):
        # 删除存在的key
        self.redispy.set(self.key.name, self.value)

        self.key.delete()
        self.assertFalse(self.key.exists)

        # 删除不存在的key，沉默
        self.assertIsNone(self.key.delete())

    def test_delete_raises(self):  
        with self.assertRaises(AssertionError):
            self.key.delete()
            raise AssertionError    # :(

    # expire

    def test_set_expire(self):
        # 对存在key进行expire
        self.redispy.set(self.key.name, self.value)

        self.assertIsNone(self.key.expire(30000))

        self.assertIsNotNone(self.key.ttl)

    def test_set_expire_raises(self):
        # 对不存在key进行expire
        with self.assertRaises(TypeError):
            self.key.expire(30000)

    # expireat

    def test_expireat(self):
        # 对存在的key进行expireat
        self.redispy.set(self.key.name, self.value)

        self.assertIsNone(self.key.expireat(1355292000))
        self.assertIsNotNone(self.key.ttl)

    def test_expireat_raise(self):
        # 对不存在的key进行expireat
        with self.assertRaises(TypeError):
            self.key.expireat(1355292000)   # 2012.12.12

    # persist

    def test_persist(self):
        # 对不存在的key进行persist
        with self.assertRaises(Exception):
            self.key.persist()

        # 对存在且没有ttl的值进行persist
        self.redispy.set(self.key.name, self.value)

        self.assertIsNone(self.key.persist())

        # 对存在且有ttl的值进行persist
        self.key.expire(3000)

        self.assertIsNone(self.key.persist())
        self.assertIsNone(self.key.ttl)


    # helper function

    def test_get_key_name_from_single_value_with_key_object(self):
        self.assertEqual(
            get_key_name_from_single_value(self.key),
            self.key.name)

    def test_get_key_name_from_single_value_with_key_name(self):
        self.assertEqual(
            get_key_name_from_single_value(self.key.name),
            self.key.name)

    def test_get_key_name_from_list_with_key_objects(self):
        self.assertListEqual(
            get_key_name_from_list([self.key]),
            [self.key.name])

    def test_get_key_name_from_list_with_key_names(self):
        self.assertListEqual(
            get_key_name_from_list([self.key.name]),
            [self.key.name])

if __name__ == "__main__":
    unittest.main()
