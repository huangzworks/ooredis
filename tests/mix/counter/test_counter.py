# coding: utf-8

import redis
import unittest

from ooredis.client import connect
from ooredis.mix.helper import format_key
from ooredis.mix.counter import Counter

class TestCounter(unittest.TestCase):
    
    def setUp(self):
        connect()

        self.redispy = redis.Redis()
        self.redispy.flushdb()

        self.tearDown()

        self.str = 'str'

        self.name = 'counter'
        self.value = 10086

        self.counter = Counter(self.name)

    def tearDown(self):
        self.redispy.flushdb()

    def set_wrong_type(self, key_object):
        self.redispy.set(key_object.name, 'string')

    # __repr__

    def test_repr_when_NOT_EXISTS(self):
        self.assertEqual(
            repr(self.counter),
            format_key(self.counter, self.name, str(None))
        )

    def test_repr_when_EXISTS(self):
        self.counter.set(self.value)
        
        self.assertEqual(
            repr(self.counter),
            format_key(self.counter, self.name, self.value)
        )
        
    # incr

    def test_incr(self):
        self.assertEqual(
            self.counter.incr(),
            1
        )

    def test_incr_with_INCREMENT(self):
        self.assertEqual(
            self.counter.incr(2),
            2
        )

    def test_incr_RAISE_when_INPUT_TYPE(self):
        with self.assertRaises(TypeError):
            self.counter.incr(self.str)

    def test_incr_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.counter)
            self.counter.incr()

    # decr

    def test_decr(self):
        self.assertEqual(
            self.counter.decr(),
            -1
        )

    def test_decr_with_DECREMENT(self):
        self.assertEqual(
            self.counter.decr(2),
            -2
        )

    def test_decr_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.counter.decr(self.str)

    def test_decr_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.counter)
            self.counter.decr()

    # iadd

    def test_iadd(self):
        self.counter += 1

        self.assertEqual(
            self.counter.get(),
            1
        )

    def test_iadd_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.counter += self.str

    def test_iadd_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.counter)
            self.counter += 1

    # isub

    def test_isub(self):
        self.counter -= 1

        self.assertEqual(
            self.counter.get(),
            -1
        )

    def test_isub_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.counter -= self.str

    def test_isub_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.counter)
            self.counter -= 1

    # get
    def test_get(self):
        self.counter.set(self.value)

        self.assertEqual(
            self.counter.get(),
            self.value
        )

    def test_get_RETURN_NONE_when_NOT_EXISTS(self):
        self.assertIsNone(
            self.counter.get()
        )

    def test_get_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.counter)
            self.counter.get()

    # set

    def test_set(self):
        self.counter.set(self.value)
        self.assertEqual(
            self.counter.get(),
            self.value
        )

    def test_set_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.counter.set(self.str) 

    # getset

    def test_getset_when_NOT_EXISTS(self):
        previous_value = self.counter.getset(self.value)

        self.assertIsNone(
            previous_value
        )

        self.assertEqual(
            self.counter.get(),
            self.value
        )

    def test_getset_when_EXISTS(self):
        self.counter.getset(self.value)

        self.new_value = 123
        previous_value = self.counter.getset(self.new_value)

        self.assertEqual(
            previous_value,
            self.value
        )

        self.assertEqual(
            self.counter.get(),
            self.new_value
        )

    def test_getset_RAISE_when_INPUT_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.counter.getset(self.str)
