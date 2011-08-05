#! /usr/bin/env python2.7
# coding: utf-8

import unittest
import redis

from ooredis.client import connect

from ooredis.mix.dict import Dict

class TestDict(unittest.TestCase):
    
    def setUp(self):
        connect()
        self.d = Dict('dict')

        self.redispy = redis.Redis()
        self.redispy.flushdb()

    def tearDown(self): 
        self.redispy.flushdb()

    # __repr__

    def test_repr(self):
        self.assertIsNotNone(repr(self.d))

    # __setitem__

    def test_setitem_and_getitem(self):
        self.d['key'] = 'value'
        self.assertEqual(self.d['key'], 'value')
        self.assertEqual(dict(self.d), {'key': 'value'})

    def test_set_a_not_exists_key_object(self):
        self.assertFalse(self.d.exists)

        self.d['key'] = 'value'
        self.assertEqual(self.d['key'], 'value')

    def test_set_overwrite_a_exists_key(self):
        self.d['key'] = 'old'
        self.assertEqual(self.d['key'], 'old')

        self.d['key'] = 'new'
        self.assertEqual(self.d['key'], 'new')

    def test_set_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d['key'] = 'value'

    # __getitem__

    def test_get(self):
        self.d['key'] = 'value'
        self.assertEqual(self.d['key'], 'value')

    def test_get_a_not_exists_key_object(self):
        with self.assertRaises(KeyError):
            self.d['key']

    def test_get_a_exists_key_object_and_not_exists_key(self):
        with self.assertRaises(KeyError):
            self.d['key'] = 'value'
            self.d['another_key']

    def test_get_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d['key']

    # __delitem__

    def test_del_not_exists_key(self):
        del self.d['a']
        self.assertEqual(dict(self.d), {})

    def test_del_exists_key(self):
        self.d['key'] = 'value'

        del self.d['key']
        self.assertTrue('key' not in self.d)
        self.assertEqual(dict(self.d), {})

    def test_del_raise_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'a string key object')
            del self.d['a']

    # __len__

    def test_len(self):
        self.assertEqual(len(self.d), 0)

        self.d['key'] = 'value'
        self.assertEqual(len(self.d), 1)

    def test_len_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            len(self.d)

    # __iter__

    def test_iter(self):
        self.assertListEqual(list(self.d), [])

        self.d['key'] = 'value'
        self.assertListEqual(list(self.d), ['key'])

    def test_iter_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            list(self.d)

    # incr

    def test_incr(self):
        self.assertEqual(self.d.incr('counter', 1), 1)

        self.assertEqual(self.d['counter'], 1)

    def test_incr_with_exists_key(self):
        self.d['counter'] = 10086

        self.assertEqual(self.d.incr('counter', 1), 10086+1)
        self.assertEqual(self.d['counter'], 10086+1)

    def test_incr_with_default_increment(self):
        self.assertEqual(self.d.incr('counter'), 1)

        self.assertEqual(self.d['counter'], 1)

    def test_incr_raise_when_key_wrong_type(self):
        with self.assertRaises(KeyError):
            self.d['string'] = 'hello'
            self.d.incr('string')

    def test_incr_raise_when_key_object_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d.incr('counter')

    # decr

    def test_decr(self):
        self.assertEqual(self.d.decr('counter', 1), -1)

        self.assertEqual(self.d['counter'], -1)

    def test_decr_with_exists_key(self):
        self.d['counter'] = 10086

        self.assertEqual(self.d.decr('counter', 1), 10086-1)
        self.assertEqual(self.d['counter'], 10086-1)

    def test_decr_with_default_decrement(self):
        self.assertEqual(self.d.decr('counter'), -1)
        self.assertEqual(self.d['counter'], -1)

    def test_decr_raise_when_key_wrong_type(self):
        with self.assertRaises(KeyError):
            self.d['string'] = 'hello'
            self.d.decr('string')

    def test_incr_raise_when_key_object_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d.decr('counter')
 
    # MAXIN method.........................

    # __contains__

    def test_in(self):
        self.assertFalse('key' in self.d)

        self.d['key'] = 'value'
        self.assertTrue('key' in self.d)

    def test_not_in(self):
        # key not in d
        self.assertTrue('key' not in self.d)

        self.d['key'] = 'value'
        self.assertFalse('key' not in self.d)

    def test_in_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            'a' in self.d

    # keys

    def test_keys(self):
        self.assertListEqual(list(self.d.keys()), [])

        self.d['key'] = 'value'
        self.assertListEqual(list(self.d.keys()), ['key'])

    def test_keys_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d.keys()

    # values

    def test_values(self):
        self.assertListEqual(list(self.d.values()), [])

        self.d['key'] = 'value'
        self.assertListEqual(list(self.d.values()), ['value'])

    def test_values_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d.values()

    # items

    def test_items(self):
        self.assertListEqual(list(self.d.items()), [])

        self.d['key'] = 'value'
        self.assertListEqual(list(self.d.items()), [('key', 'value')])

    def test_items_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d.items()

    # get

    def test_get(self):
        self.assertEqual(self.d.get('key', 'default'), 'default')

        self.d['key'] = 'value'
        self.assertEqual(self.d.get('key', 'default'), 'value')

    def test_get_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d.get('a')

    # __eq__ and __neq__ not raise TypeError

    def test_eq(self):
        # d == d
        self.assertEqual(self.d, self.d)
    
        # same value, different key, not equal in ooredis
        self.another_d = Dict('another_d')
        self.assertNotEqual(self.d, self.another_d)

    def test_not_eq(self):
        # d != another_d
        self.another_d = Dict('another_d')
        self.assertNotEqual(self.d, self.another_d)

    # pop

    def test_pop(self):
        self.d['key'] = 'value'
        self.assertEqual(self.d.pop('key'), 'value')

    def  test_pop_key_not_exists_but_default_set(self):
        self.assertEqual(self.d.pop('key', 'default'), 'default')

    def test_pop_raise_when_key_not_exists_and_no_default(self):
        with self.assertRaises(KeyError):
            self.d.pop('key')

    def test_pop_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d.pop('a', 'default')

    # popitem

    def test_popitem(self):
        self.d['key'] = 'value'
        self.assertEqual(self.d.popitem(), ('key', 'value'))

        self.d['key'] = 'value'
        self.d['name'] = 'huangz'
        self.pop = self.d.popitem()
        self.assertTrue(self.pop == ('key', 'value') or \
                        self.pop == ('name', 'huangz'))

        self.assertEqual(len(self.d), 1)

    def test_popitem_raise_when_dict_empty(self):
        with self.assertRaises(KeyError):
            self.d.popitem()

    def test_popitem_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d.popitem()

    # clear

    def test_clear_in_not_empty_dict(self):
        self.d['key'] = 'value'
        self.assertEqual(len(self.d), 1)

        self.d.clear()
        self.assertEqual(len(self.d), 0)

    def test_clear_in_empty_dict(self):
        self.d.clear()
        self.assertEqual(len(self.d), 0)

    def test_clear_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d.clear()
       
    # update

    def test_update_not_exists_key(self):
        self.data = {'key': 'value'}

        self.d.update(self.data)

        self.assertEqual(self.d.popitem(),
                         self.data.popitem())

    def test_update_exists_key(self):
        self.d['key'] = 'old'

        self.data = {'key': 'value'}
        self.d.update(self.data)

        self.assertEqual(self.d.popitem(),
                         self.data.popitem())

    def test_update_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d.update({'key': 'value'})

    # setdefault

    def test_setdefault_with_not_exists_key(self):
        self.assertEqual(self.d.setdefault('key', 'value'),
                         'value')
        self.assertEqual(self.d['key'], 'value')

    def test_setdefault_with_exists_key(self):
        self.d['key'] = 'old_value'

        # assignment false
        self.assertEqual(self.d.setdefault('key', 'new_value'),
                         'old_value')
        
        # old_value not change
        self.assertEqual(self.d['key'], 'old_value')

    def test_setdefault_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.d.name, 'string')
            self.d.setdefault('key', 'default')

if __name__ == "__main__":
    unittest.main()
