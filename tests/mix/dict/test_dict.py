#! /usr/bin/env python2.7
# coding: utf-8

import redis
import unittest

from ooredis.client import connect
from ooredis.mix.dict import Dict
from ooredis.mix.helper import format_key

class TestDict(unittest.TestCase):
    
    def setUp(self):
        connect()

        self.redispy = redis.Redis()
        self.redispy.flushdb()

        self.name = 'dict'
        self.key = 'key'
        self.value = 'value'

        self.d = Dict(self.name)

    def tearDown(self): 
        self.redispy.flushdb()

    # __repr__

    def test__repr__(self):
        assert repr(self.d) == format_key(self.d, self.name, dict(self.d))

    # __setitem__

    def test__setitem__with_NOT_EXISTS_KEY(self):
        self.d[self.key] = self.value
        
        assert self.d[self.key] == self.value
        assert dict(self.d) == {self.key: self.value}

    def test__setitem__OVERWRITE_EXISTS_KEY(self):
        self.old_value = 'foo'

        self.d[self.key] = self.old_value
        assert self.d[self.key] == self.old_value

        self.d[self.key] = self.value
        assert self.d[self.key] == self.value

    def test__setitem__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d[self.key] = self.value

    # __getitem__

    def test__getitem__with_EXISTS_KEY(self):
        self.d[self.key]= self.value

        assert self.d[self.key] == self.value

    def test__getitem__RAISE_when_KEY_NOT_EXISTS(self):
        with self.assertRaises(KeyError):
            self.d[self.key]

    def test__getitem__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d[self.key]

    # __delitem__

    def test__delitem__when_KEY_EXISTS(self):
        self.d[self.key] = self.value
        
        del self.d[self.key]

        assert self.key not in self.d
        assert dict(self.d) == {}

    def test__delitem__when_KEY_NOT_EXISTS(self):
        with self.assertRaises(KeyError):
            del self.d['not_exists_key']

    def test__delitem__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'a string key object')
            del self.d['wrong_type_cant_be_set']

    # __iter__

    def test__ite__with_EMPTY_DICT(self):
        assert list(iter(self.d)) == []

    def test__ite__with_NOT_EMPTY_DICT(self):
        self.d[self.key] = self.value
        assert list(iter(self.d)) == [self.key]

    def test__iter__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            list(iter(self.d))

    # __len__

    def test__len__with_EMPTY_DICT(self):
        assert len(self.d) == 0

    def test__len__with_NOT_EMPTY_DICT(self):
        self.d[self.key] = self.value

        assert len(self.d) == 1

    def test__len__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            len(self.d)

if __name__ == "__main__":
    unittest.main()
