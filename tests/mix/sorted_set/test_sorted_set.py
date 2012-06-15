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

    def set_wrong_type(self):
        self.redispy.set(self.s.name, 'string')


    # __repr__

    def test_repr(self):
        self.assertEqual(
            repr(self.s),
            format_key(self.s, self.s.name, list(self.s))
        )


    # __len__

    def test_len_RETURN_0_when_SET_EMPTY(self):
        self.assertEqual(len(self.s), 0)

    def test_len_with_NOT_EMPTY_SET(self):
        self.s[self.element] = self.score

        self.assertEqual(
            len(self.s),
            1
        )

    def test_len_RAISE_when_WONRG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type()
            len(self.s)


    # __contains__

    def test_in_RETURN_FALSE(self):
        self.assertFalse(
            self.element in self.s
        )

    def test_in_RETURN_TRUE(self):
        self.s[self.element] = self.score

        self.assertTrue(
            self.element in self.s
        )

    def test_in_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type()
            self.element in self.s


    # __setitem__

    def test_setitem_when_MEMBER_NOT_EXISTS(self):
        self.s[self.element] = self.score

        self.assertEqual(
            len(self.s),
            1
        )

        self.assertEqual(
            self.s[0]['value'],
            self.element
        )
        self.assertEqual(
            self.s[0]['score'], 
            self.score
        )

    def test_setitem_UPDATE_SCORE_when_MEMBER_EXISTS(self):
        self.s[self.element] = 10086

        self.s[self.element] = self.score

        self.assertEqual(
            self.s[0]['value'],
            self.element
        )
        self.assertEqual(
            self.s[0]['score'],
            self.score
        )

    def test_setitem_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type()
            self.s[self.element] = self.score


    # __getitem__

    def test_getitem_with_INDEX(self):
        self.s[self.element] = self.score

        self.assertTrue(
            isinstance(self.s[0], dict)
        )

        self.assertEqual(
            self.s[0]['value'],
            self.element
        )
        self.assertEqual(
            self.s[0]['score'],
            self.score
        )

    def test_getitem_RAISE_when_INDEX_OUT_OF_RANGE(self):
        with self.assertRaises(IndexError):
            self.s[10086]

    def test_getitem_with_RANGE(self):
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
            self.set_wrong_type()
            self.s[:]


    # __delitem__

    def test__delitem__(self):
        self.s[self.element] = self.score

        del self.s[0]

        self.assertEqual(
            len(self.s),
            0
        )

    def test__delitem__with_EMPTY_SET(self):
        del self.s[:]
        self.assertEqual(
            len(self.s),
            0
        )

    def test__delitem__with_DEFAULT_START_OR_DEFAULT_END_RANGE(self):
        self.s['one'] = 1
        self.s['two'] = 2
        self.s['three'] = 3

        # del 'one'
        del self.s[:1]

        self.assertEqual(
            len(self.s),
            2
        )
        self.assertEqual(
            self.s[:],
            [
                {'value': 'two', 'score': 2},
                {'value': 'three', 'score': 3},
            ]
        )

        # del 'three'
        del self.s[1:]

        self.assertEqual(
            len(self.s),
            1
        )
        self.assertEqual(
            self.s[:],
            [
                {'value': 'two', 'score': 2},
            ]
        )

        # del all
        del self.s[:]
        self.assertEqual(
            len(self.s), 
            0
        )

    def test__delitem__with_REVERSE_RANGE(self):
        self.s['one'] = 1
        self.s['two'] = 2
        self.s['three'] = 3

        # del 'three'
        del self.s[-1]

        self.assertEqual(
            len(self.s), 
            2
        )
        self.assertEqual(
            self.s[:],
            [
                {'value': 'one', 'score': 1},
                {'value': 'two', 'score': 2}
            ]
        )

        # del 'two'
        del self.s[-1:]

        self.assertEqual(
            len(self.s), 
            1
        )
        self.assertEqual(
            self.s[:],
            [
                {'value': 'one', 'score': 1}
            ]
        )

        # del 'one'
        del self.s[-1]
        self.assertEqual(
            len(self.s), 
            0
        )

    def test__delitem__in_RANGE_with_GIVEN_START_AND_END(self):
        self.s['one'] = 1

        del self.s[0:1]

        self.assertEqual(
            len(self.s), 
            0
        )

    def test__delitem__RAISE_when_INDEX_OUT_OF_RANGE(self):
        with self.assertRaises(IndexError):
            del self.s[10086]
    
    def test__delitem__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type()
            del self.s[:]


    # remove

    def test_remove_EXISTS_MEMBER(self):
        self.s[self.element] = self.score

        self.s.remove(
            self.element
        )
        self.assertEqual(
            len(self.s),
            0
        )

    def test_remove_NOT_EXISTS_MEMBER_with_DEFAULT_CHECK(self):
        self.s.remove(self.element) # check=False

    def test_remove_NOT_EXISTS_MEMBER_with_CHECK_OFF(self):
        self.s.remove(self.element, check=False)

    def test_remove_NOT_EXISTS_MEMBER_with_CHECK_ON(self):
        with self.assertRaises(KeyError):
            self.s.remove(self.element, check=True)

    def test_remove_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type()
            self.s.remove(self.element)


    # rank

    def test_rank(self):

        self.s[self.element] = self.score

        self.assertEqual(
            self.s.rank(self.element), 
            0
        )

        # 插入一个 score 值比 self.element 更小的元素
        self.s['new'] = self.score-1
        # self.element被重排了
        self.assertEqual(
            self.s.rank(self.element), 
            1
        )
    
    def test_rank_in_REVERSE_OREDER(self):

        self.s[self.element] = self.score

        self.assertEqual(
            self.s.rank(self.element, reverse=True),
            0
        )

        # 插入一个score值比self.element更大的元素
        self.s['new'] = self.score+1
        # self.element被重排了
        self.assertEqual(
            self.s.rank(self.element, reverse=True),
            1
        )

    def test_rank_RAISE_when_MEMBER_NOT_EXISTS(self):
        with self.assertRaises(KeyError):
            self.s.rank(self.element)

    def test_rank_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type()
            self.s.rank(self.element)


    # score

    def test_score(self):
        self.s[self.element] = self.score

        self.assertEqual(
            self.s.score(self.element), 
            self.score
        )

    def test_score_RAISE_when_MEMBER_NOT_EXISTS(self):
        with self.assertRaises(KeyError):
            self.s.score(self.element)

    def test_score_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type()
            self.s.score(self.element)


    # incr

    def test_incr_RETURN_FALOT_TYPE(self):
        self.assertTrue(
            isinstance(self.s.incr(self.element), float)
        )

    def test_incr_with_EXISTS_MEMBER(self):
        self.s[self.element] = self.score

        self.increment = 100

        self.assertEqual(
            self.s.incr(self.element, self.increment),
            self.score + self.increment
        )

    def test_incr_with_EXISTS_MEMBER_using_DEFAULT_INCREMENT(self):
        self.s[self.element] = self.score

        self.default_increment = 1

        self.assertEqual(
            self.s.incr(self.element),
            self.score + self.default_increment
        )

    def test_incr_with_NOT_EXISTS_MEMBER(self):
        self.assertEqual(
            self.s.incr(self.element), 
            1
        )

        self.assertEqual(
            len(self.s), 
            1
        )
        self.assertEqual(
            self.s.score(self.element),
            1
        )

    def test_incr_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type()
            self.s.incr(self.element)

    # decr

    def test_decr_RETURN_FALOT_TYPE(self):
        self.assertTrue(
            isinstance(self.s.decr(self.element), float)
        )

    def test_decr_with_EXISTS_MEMBER(self):
        self.s[self.element] = self.score

        self.decrement = 100

        self.assertEqual(
            self.s.decr(self.element, self.decrement),
            self.score - self.decrement
        )

    def test_decr_with_EXISTS_MEMBER_using_DEFAULT_DECREMENT(self):
        self.s[self.element] = self.score

        self.default_decrement = 1

        self.assertEqual(
            self.s.decr(self.element),
            self.score-self.default_decrement
        )

    def test_decr_with_NOT_EXISTS_MEMBER(self):
        self.assertEqual(
            self.s.decr(self.element),
            -1
        )

        self.assertEqual(
            len(self.s),
            1
        )
        self.assertEqual(
            self.s.score(self.element),
            -1
        )
    
    def test_decr_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type()
            self.s.decr(self.element)


if __name__ == "__main__":
    unittest.main()
