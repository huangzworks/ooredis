#! /usr/bin/env python2.7
# coding: utf-8

import redis
import unittest

from ooredis.client import connect
from ooredis.mix.helper import format_key
from ooredis.mix.sorted_set import SortedSet
    
class TestSortedSet(unittest.TestCase):

    def setUp(self):
        connect()

        self.redispy = redis.Redis()
        self.redispy.flushdb()

        self.s = SortedSet('sorted_set')
        self.another = SortedSet('another')

        self.element = 'value'
        self.score = 10086
        
    def tearDown(self):
        self.redispy.flushdb()

    # __repr__

    def test_repr(self):
        self.assertEqual(repr(self.s),
                         format_key(self.s, self.s.name, list(self.s)))

    # __len__

    def test_len_with_empty_set(self):
        self.assertEqual(len(self.s), 0)

    def test_len_with_not_empty_set(self):
        self.s[self.element] = self.score

        self.assertEqual(len(self.s), 1)

    def test_len_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.s.name, 'string')
            len(self.s)

    # __contains__

    def test_in_with_empty_set(self):
        self.assertFalse(self.element in self.s)

    def test_in_with_not_empty_set(self):
        self.s[self.element] = self.score

        self.assertTrue(self.element in self.s)

    def test_in_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.s.name, 'string')
            self.element in self.s


    # __setitem__

    def test_setitem(self):
        self.s[self.element] = self.score

        self.assertEqual(len(self.s), 1)

        self.assertEqual(self.s[0]['value'], self.element)
        self.assertEqual(self.s[0]['score'], self.score)

    def test_setitem_overwrite(self):
        self.s[self.element] = self.score

        self.s[self.element] = 123123

        self.assertEqual(self.s[0]['value'], self.element)
        self.assertEqual(self.s[0]['score'], 123123)

    def test_setitem_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.s.name, 'string')
            self.s[self.element] = self.score

    # __getitem__

    def test_getitem(self):
        self.s[self.element] = self.score

        self.assertTrue(isinstance(self.s[0], dict))

        self.assertEqual(self.s[0]['value'], self.element)
        self.assertEqual(self.s[0]['score'], self.score)

    def test_getitem_index_out_of_range(self):
        with self.assertRaises(IndexError):
            self.s[10086]

    def test_getitem_with_range(self):
        self.s['one'] = 1
        self.s['two'] = 2
        self.s['three']= 3

        self.assertEqual(self.s[1:],    
                         [{'value': 'two', 'score': 2},
                          {'value': 'three', 'score': 3},])

        self.assertEqual(self.s[:2],
                        [{'value': 'one', 'score': 1},
                         {'value': 'two', 'score': 2}])

        self.assertEqual(self.s[:],
                        [{'value': 'one', 'score': 1},
                         {'value': 'two', 'score': 2},
                         {'value': 'three', 'score': 3},])

        self.assertEqual(self.s[1:2],
                         [{'value': 'two', 'score': 2},])

        self.assertEqual(self.s[10086:],
                         [])

    def test_getitem_with_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.s.name, 'string')
            self.s[:]

    # __delitem__

    def test_delitem(self):
        self.s[self.element] = self.score

        del self.s[0]
        self.assertEqual(len(self.s), 0)

    def test_delitem_with_empty_set(self):
        del self.s[:]
        self.assertEqual(len(self.s), 0)

    def test_delitem_with_range_and_default_start_or_default_end(self):
        self.s['one'] = 1
        self.s['two'] = 2
        self.s['three'] = 3

        # del 'one'
        del self.s[:1]

        self.assertEqual(len(self.s), 2)
        self.assertEqual(self.s[:],
                         [{'value': 'two', 'score': 2},
                          {'value': 'three', 'score': 3},])

        # del 'three'
        del self.s[1:]

        self.assertEqual(len(self.s), 1)
        self.assertEqual(self.s[:],
                         [{'value': 'two', 'score': 2},])

        # del all
        del self.s[:]
        self.assertEqual(len(self.s), 0)

    def test_delitem_with_reverse_range(self):
        self.s['one'] = 1
        self.s['two'] = 2
        self.s['three'] = 3

        # del 'three'
        del self.s[-1]

        self.assertEqual(len(self.s), 2)
        self.assertEqual(self.s[:],
                         [{'value': 'one', 'score': 1},
                          {'value': 'two', 'score': 2}])

        # del 'two'
        del self.s[-1:]

        self.assertEqual(len(self.s), 1)
        self.assertEqual(self.s[:],
                         [{'value': 'one', 'score': 1}])

        # del 'one'
        del self.s[-1]
        self.assertEqual(len(self.s), 0)

    def test_delitem_with_range_and_given_start_and_end(self):
        self.s['one'] = 1

        del self.s[0:1]
        self.assertEqual(len(self.s), 0)

    def test_delitem_raise_when_index_out_of_range(self):
        with self.assertRaises(IndexError):
            del self.s[10086]
    
    def test_delitem_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.s.name, 'string')
            del self.s[:]

    # remove

    def test_remove_with_exists_member(self):
        self.s[self.element] = self.score

        self.s.remove(self.element)
        self.assertEqual(len(self.s), 0)

    def test_remove_with_not_exists_member_and_default_check(self):
        self.s.remove(self.element) # check=False

    def test_remove_with_not_exists_member_and_check_off(self):
        self.s.remove(self.element, check=False)

    def test_remove_with_not_exists_member_and_check_on(self):
        with self.assertRaises(KeyError):
            self.s.remove(self.element, check=True)

    def test_remove_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.s.name, 'string')
            self.s.remove(self.element)

    # rank

    def test_rank(self):
        self.s[self.element] = self.score
        self.assertEqual(self.s.rank(self.element), 0)

        # 插入一个score值比self.element更小的元素
        self.s['new'] = self.score-1
        # self.element被重排了
        self.assertEqual(self.s.rank(self.element), 1)
    
    def test_rank_in_reverse_order(self):
        self.s[self.element] = self.score
        self.assertEqual(self.s.rank(self.element, reverse=True),
                         0)

        # 插入一个score值比self.element更大的元素
        self.s['new'] = self.score+1
        # self.element被重排了
        self.assertEqual(self.s.rank(self.element, reverse=True),
                         1)

    def test_rank_raise_when_member_not_exists(self):
        with self.assertRaises(KeyError):
            self.s.rank(self.element)

    def test_rank_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.s.name, 'string')
            self.s.rank(self.element)

    # score

    def test_score(self):
        self.s[self.element] = self.score

        self.assertEqual(self.s.score(self.element), self.score)

    def test_score_raise_when_member_not_exist(self):
        with self.assertRaises(KeyError):
            self.s.score(self.element)

    def test_score_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.s.name, 'string')
            self.s.score(self.element)

    # incr

    def test_incr_return_float_type(self):
        self.assertTrue(isinstance(self.s.incr(self.element), float))

    def test_incr_with_exists_member(self):
        self.s[self.element] = self.score

        self.increment = 100

        self.assertEqual(self.s.incr(self.element, self.increment),
                         self.score + self.increment)

    def test_incr_with_exists_member_and_default_increment(self):
        self.s[self.element] = self.score

        self.default_increment = 1

        self.assertEqual(self.s.incr(self.element),
                         self.score + self.default_increment)

    def test_incr_with_not_exists_member(self):
        self.assertEqual(self.s.incr(self.element), 1)

        self.assertEqual(len(self.s), 1)
        self.assertEqual(self.s.score(self.element), 1)

    def test_incr_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.s.name, 'string')
            self.s.incr(self.element)

    # decr

    def test_decr_return_float_type(self):
        self.assertTrue(isinstance(self.s.decr(self.element), float))

    def test_decr_with_exists_member(self):
        self.s[self.element] = self.score

        self.decrement = 100

        self.assertEqual(self.s.decr(self.element, self.decrement),
                         self.score - self.decrement)

    def test_decr_with_exists_member_and_default_decrement(self):
        self.s[self.element] = self.score

        self.default_decrement = 1

        self.assertEqual(self.s.decr(self.element),
                         self.score-self.default_decrement)

    def test_decr_with_not_exists_member(self):
        self.assertEqual(self.s.decr(self.element),
                         -1)

        self.assertEqual(len(self.s), 1)
        self.assertEqual(self.s.score(self.element),
                         -1)
    
    def test_decr_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.s.name, 'string')
            self.s.decr(self.element)

if __name__ == "__main__":
    unittest.main()
