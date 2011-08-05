#! /usr/bin/env python2.7
# coding: utf-8

import unittest
import redis

from ooredis.client import connect

from ooredis.mix.list import List

class TestList(unittest.TestCase):
    
    def setUp(self):
        connect()
        self.l = List('list')
        self.destination = List('destination')

        self.redispy = redis.Redis()
        self.redispy.flushdb()

    def tearDown(self):
        self.redispy.flushdb()

    # __repr__

    def test_repr(self):
        self.assertIsNotNone(repr(self.l))

    # len

    def test_len_with_empty_list(self):
        self.assertEqual(len(self.l), 0)
        
    def test_len_with_not_empty_list(self):
        self.l.lpush('item')
        self.assertEqual(len(self.l), 1)

    def test_len_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.l.name, 'string')
            len(self.l)

    # lpush & lpop

    def test_lpush_and_lpop(self):
        self.l.lpush('item')
        self.assertEqual(self.l.lpop(), 'item')

    def test_lpush_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.l.name, 'string')
            self.l.lpush('item')

    def test_lpop_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.l.name, 'string')
            self.l.lpop()

    def test_lpop_raise_when_empty_list(self):
        with self.assertRaises(IndexError):
            self.l.lpop()

    # blpop

    def test_blpop_with_not_empty_list(self):
        self.l.lpush('item')
        self.assertEqual(self.l.blpop(), 'item')

    def test_blpop_with_empty_list(self):
        self.assertIsNone(self.l.blpop(timeout=1))

    def test_blpop_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set('list', 'string')
            self.l.blpop()

    # rpush & rpop

    def test_rpush_and_rpop(self):
        self.l.rpush('item')
        self.assertEqual(self.l.rpop(), 'item')

    def test_rpush_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.l.name, 'string')
            self.l.rpush('item')

    def test_rpop_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.l.name, 'string')
            self.l.rpop()

    def test_rpop_raise_when_empty_list(self):
        with self.assertRaises(IndexError):
            self.l.rpop()
    
    # brpop

    def test_brpop_in_not_empty_list(self):
        self.l.rpush('item')
        self.assertEqual(self.l.brpop(), 'item')

    def test_brpop_in_empty_list(self):
        self.assertIsNone(self.l.brpop(timeout=1))

    def test_brpop_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.l.name, 'string')
            self.l.brpop()

    # __setitem__

    def test_setitem(self):
        self.l.lpush('item')

        self.l[0] = 'value'
        self.assertEqual(self.l.lpop(), 'value')

    def test_setitem_raise_when_out_of_range(self):
        with self.assertRaises(IndexError):
            self.l.lpush('value') 
            self.l[10086] = 'items'

    def test_setitem_raise_when_key_not_exists(self):
        with self.assertRaises(IndexError):
            self.l[0] = 'value'

    def test_setitem_raise_when_using_range_assignment(self):
        with self.assertRaises(NotImplementedError):
            self.l.lpush('one')
            self.l.lpush('two')
            self.l[:] = ['hello']

    def test_setitem_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.l.name, 'string')
            self.l[0] = 'value'
    
    # __getitem__

    def test_geitem(self):
        self.l.lpush('item')
        self.assertEqual(self.l[0], 'item')

    def test_getitem_with_not_exists_key(self):
        with self.assertRaises(IndexError):
            self.l[0]

    def test_getitem_raise_when_index_out_of_range(self):
        with self.assertRaises(IndexError):
            self.l.lpush('item')
            self.l[10086]

    def test_getitem_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.l.name, 'string')
            self.l[10086]

    def test_getitem_with_range(self):
        self.t = ['one' ,'two']

        self.l.rpush('one')
        self.l.rpush('two')

        # l[:]
        self.assertListEqual(list(self.l), ['one', 'two'])
        self.assertListEqual(list(self.l), list(self.t))

        # l[0:]
        self.assertEqual(self.l[0:], ['one', 'two'])
        self.assertEqual(self.l[0:], self.t[0:])

        # l[:1]
        self.assertEqual(self.l[:1], ['one'])
        self.assertEqual(self.l[:1], self.t[:1])

        # l[0:0]
        self.assertEqual(self.l[0:0], [])
        self.assertEqual(self.l[0:0], self.t[0:0])

        # l[0:1]
        self.assertEqual(self.l[0:1], ['one'])
        self.assertEqual(self.l[0:1], self.t[0:1])

        # l[0:2]
        self.assertEqual(self.l[0:2], ['one', 'two'])
        self.assertEqual(self.l[0:2], self.t[0:2])

        # l[-2:-1]
        self.assertEqual(self.l[-2:-1], ['one'])
        self.assertEqual(self.l[-2:-1], self.t[-2:-1])

        # l[-1:-1]
        self.assertEqual(self.l[-1:-1], [])
        self.assertEqual(self.l[-1:-1], self.t[-1:-1])

        # l[:10086]
        self.assertEqual(self.l[:10086], ['one', 'two'])
        self.assertEqual(self.l[:10086], self.t[:10086])

        # l[10086:]
        self.assertEqual(self.l[10086:], [])
        self.assertEqual(self.l[10086:], self.t[10086:])

    # __delitem__

    def test_delitem(self):
        self.l.rpush('a')
        self.l.rpush('b')
        self.l.rpush('c')
        self.l.rpush('d')

        # del tail('c', 'd')
        del self.l[2:]
        self.assertEqual(list(self.l), ['a', 'b'])

        # del head('a')
        del self.l[:1]
        self.assertEqual(list(self.l), ['b'])
    
        # del all
        del self.l[:]
        self.assertEqual(list(self.l), [])

        # del list[x:y] 
        # not support yet
        with self.assertRaises(NotImplementedError):
            del self.l[0:1]

        # del list[x]
        # not support yet
        with self.assertRaises(NotImplementedError):
            del self.l[0]

    def test_delitem_out_of_range(self):
        self.l.rpush('a')
        self.l.rpush('b')

        del self.l[10086:]
        self.assertEqual(list(self.l), ['a', 'b'])

        del self.l[:10086]
        self.assertEqual(list(self.l), [])

    def test_delitem_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.l.name, 'string')
            del self.l[:]

    # rpoplpush

    def test_rpoplpush_with_empty_list(self):
        self.destination = List('destination')
        
        self.assertIsNone(self.l.rpoplpush(self.destination.name))
        
        self.assertEqual(len(self.l), 0)
        self.assertEqual(len(self.destination), 0)

    def test_rpoplpush_with_not_empty_list(self):
        self.l.lpush('item')
        self.destination = List('destination')

        self.assertEqual(
            self.l.rpoplpush(self.destination.name),
            'item')

        self.assertEqual(len(self.l), 0)
        self.assertEqual(len(self.destination), 1)
        self.assertEqual(self.destination[0], 'item')

    def test_rpoplpush_do_rpop_and_lpush_right(self):
        # BEFORE rpoplpush:
        # self.l = ['safe', 'pop_element']
        # self.destination = ['safe']
        #
        # AFTER rpoplpush:
        # self.l = ['safe']
        # self.destination = ['pop_element', 'safe']
        self.l.rpush('safe')
        self.l.rpush('pop_element')

        self.destination.rpush('safe')

        self.l.rpoplpush(self.destination.name)
        
        self.assertEqual(len(self.l), 1)
        self.assertEqual(self.l[0], 'safe')

        self.assertEqual(len(self.destination), 2)
        self.assertEqual(self.destination[0], 'pop_element')
        self.assertEqual(self.destination[1], 'safe')

    def test_rpoplpush_accept_key_object_and_key_name_as_destination(self):
        self.l.rpush('item')

        self.l.rpoplpush(self.destination) # key object
        self.assertEqual(len(self.l), 0)
        self.assertEqual(self.destination[0], 'item')

        self.destination.rpoplpush(self.l.name) # key name
        self.assertEqual(len(self.destination), 0)
        self.assertEqual(self.l[0], 'item')

    def test_rpoplpush_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.l.name, 'string')
            self.l.rpoplpush(self.destination)

    # brpoplpush

    def test_brpoplpush_with_empty_list(self):
        self.assertIsNone(self.l.brpoplpush(self.destination.name, timeout=1))

        self.assertEqual(len(self.l), 0)
        self.assertEqual(len(self.destination), 0)

    def test_brpoplpush_with_not_empty_list(self):
        self.l.rpush('item')
        
        self.assertEqual(
            self.l.brpoplpush(self.destination.name),
            'item')

        self.assertEqual(len(self.l), 0)
        self.assertEqual(self.destination[0], 'item')
        
    def test_brpoplpush_do_rpop_and_lpush_right(self):
        # before brpoplpush:
        # self.l = ['safe', 'pop_element']
        # self.destination = ['safe']
        #
        # after brpoplpush:
        # self.l = ['safe']
        # self.destination = ['pop_element', 'safe']
        self.l.rpush('safe')
        self.l.rpush('pop_element')

        self.destination.rpush('safe')

        self.l.brpoplpush(self.destination.name)
        
        self.assertEqual(len(self.l), 1)
        self.assertEqual(self.l[0], 'safe')

        self.assertEqual(len(self.destination), 2)
        self.assertEqual(self.destination[0], 'pop_element')
        self.assertEqual(self.destination[1], 'safe')

    def test_brpoplpush_accept_key_object_and_key_name_as_destination(self):
        self.l.rpush('item')

        self.l.brpoplpush(self.destination) # key object
        self.assertEqual(len(self.l), 0)
        self.assertEqual(self.destination[0], 'item')

        self.destination.brpoplpush(self.l.name) # key name
        self.assertEqual(len(self.destination), 0)
        self.assertEqual(self.l[0], 'item')

    def test_brpoplpush_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.l.name, 'string')
            self.l.brpoplpush(self.destination)

    # remove

    def test_remove_with_empty_list(self):
        self.l.remove('item')

        self.assertEqual(len(self.l), 0)

    def test_remove_with_not_empty_list(self):
        self.l.lpush('item')

        self.assertEqual(self.l.remove('item'), 1)
        self.assertEqual(len(self.l), 0)

    def test_remove_delete_multi_value(self):
        self.l.lpush('item')    # 1
        self.l.lpush('item')    # 2
        self.l.lpush('safe')    # not in group
        self.l.lpush('item')    # 3

        self.assertEqual(self.l.remove('item'), 3)
        self.assertEqual(len(self.l), 1)
        self.assertEqual(self.l[0], 'safe')

    def test_remove_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.l.name, 'string')
            self.l.remove('item')

    # MIXIN methods

    # __contains__

    def test_in(self):
        self.assertFalse('item' in self.l)

        self.l.lpush('item')
        self.assertTrue('item' in self.l)

    # __iter__

    def test_iter(self):
        self.assertListEqual(list(self.l), [])

        self.l.lpush('one')
        self.assertListEqual(list(self.l), ['one'])

        self.l.rpush('two')
        self.assertListEqual(list(self.l), ['one', 'two'])

    # __reverse__

    def test_reverse(self):
        self.assertListEqual(list(reversed(self.l)), [])

        self.l.lpush('one')
        self.assertListEqual(list(reversed(self.l)), ['one'])

        self.l.rpush('two')
        self.assertListEqual(list(reversed(self.l)), ['two', 'one'])

    # index

    def test_index(self):
        with self.assertRaises(ValueError):
            self.l.index('item')

        self.l.lpush('item')
        self.assertEqual(self.l.index('item'), 0)

    # count

    def test_count(self):
        self.assertEqual(self.l.count('item'), 0)
        
        self.l.lpush('item')
        self.assertEqual(self.l.count('item'), 1)

        self.l.lpush('item')
        self.assertEqual(self.l.count('item'), 2)
    
if __name__ == "__main__":
    unittest.main()
