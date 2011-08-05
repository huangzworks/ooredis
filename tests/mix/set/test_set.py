#! /usr/bin/env python2.7
# coding: utf-8

import unittest
import redis

from ooredis.client import connect

from ooredis.mix.key import Key
from ooredis.mix.set import Set
    
class TestSet(unittest.TestCase):

    def setUp(self):
        connect()

        self.s = Set('set')
        self.another = Set('another')
        self.third = Set('third')

        self.redispy = redis.Redis()
        self.redispy.flushdb()

    def tearDown(self):
        self.redispy.flushdb()

    # __repr__

    def test_repr(self):
        self.assertIsNotNone(repr(self.s))

    # len
    # add

    def test_add_len(self):
        self.assertEqual(len(self.s), 0)

        self.s.add('e')
        self.assertEqual(len(self.s), 1)

    def test_len_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set('set', 'string')
            len(self.s)

    def test_add_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set('set', 'string')
            self.s.add('e')

    # __iter__

    def test_iter(self):
        self.assertListEqual(list(self.s), [])

        self.s.add('e')
        self.assertListEqual(list(self.s), ['e'])

    def test_iter_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set('set', 'string')
            list(self.s)

    # in

    def test_contain(self):
        self.assertFalse('e' in self.s)

        self.s.add('e')
        self.assertTrue('e' in self.s)

    def test_contain_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set('set', 'string')
            'e' in self.s

    # remove

    def test_remove_with_empty_set(self):
        self.s.remove('e')
        self.assertEqual(len(self.s), 0)

    def test_remove_with_not_empty_set(self):
        self.s.add('e')
        self.assertEqual(len(self.s), 1)

        self.s.remove('e')
        self.assertEqual(len(self.s), 0)

    def test_remove_when_value_not_member_and_check_is_False(self):
        self.assertIsNone(self.s.remove('not_exists_key'))

    def test_remove_raise_when_value_not_member_and_check_is_True(self):
        with self.assertRaises(KeyError):
            self.s.remove('not_exists_key',check=True)

    def test_remove_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set('set', 'string')
            self.s.remove('e')

    # pop

    def test_pop_with_empty_set(self):
        with self.assertRaises(KeyError):
            self.s.pop()

    def test_pop_with_not_empty_set(self):
        self.s.add('element')

        self.assertEqual(self.s.pop(), 'element')
        self.assertEqual(len(self.s), 0)

    def test_pop_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set('set', 'string')
            self.s.pop()

    # random

    def test_random_in_empty_set(self):
        self.assertIsNone(self.s.random())

    def test_random_in_not_empty_set(self):
        self.s.add('e')
        self.assertEqual(self.s.random(), 'e')
        self.assertEqual(len(self.s), 1)

        self.s.add('b')
        self.assertTrue(self.s.random() in ['e', 'b'])

    def test_random_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set('set', 'string')
            self.s.random()

    # move

    def test_move(self):
        self.s.add('e')

        self.another = Set('another')
        self.s.move(self.another, 'e')

        # self.s empty and self.another not empty more
        self.assertEqual(len(self.s), 0)
        self.assertEqual(len(self.another), 1)

        self.assertEqual(self.another.pop(), 'e')

    def test_move_raise_key_error_when_element_not_set_member(self):
        with self.assertRaises(KeyError):
            self.s.move('another', 'e')

    def test_move_accpet_key_and_key_name_as_destination(self):
        self.s.add('a')
        self.s.add('b')

        self.s.move(self.another, 'a')
        self.assertEqual(len(self.another), 1)

        # self.another.name == 'another'
        self.s.move(self.another.name, 'b') 
        self.assertEqual(len(self.another), 2)

    def test_move_when_two_set_have_same_member(self):
        self.s.add('a')
        self.another.add('a')

        self.s.move(self.another, 'a')

        # make sure self.s's 'a' has been delete
        # and nothing change in self.another
        self.assertEqual(len(self.s), 0)
        self.assertEqual(len(self.another), 1)
        self.assertEqual(self.another.pop(), 'a')

    def test_move_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.s.name, 'string')
            self.s.move('another', 'e')

    # isdisjoint

    def test_isdisjoint_True(self):
        self.s.add('a')
        self.another.add('e')

        self.assertTrue(self.s.isdisjoint(self.another))

    def test_isdisjoint_False(self):
        self.s.add('a')
        self.another.add('a')

        self.assertFalse(self.s.isdisjoint(self.another))

    def test_idisjoint_with_set(self):
        self.s.add('a')
        
        self.set = set('a')

        self.assertFalse(self.s.isdisjoint(self.set))

    def test_isdisjoint_raise_when_other_not_key_object(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.another.name, 'string') 
            self.s.isdisjoint(self.another)

    # issubset <=

    def test_issubset_True(self):
        self.s.add('a')
        self.another.add('a')

        self.assertTrue(self.s <= self.another)

    def test_issubset_False(self):
        self.s.add('a')
        
        self.assertFalse(self.s <= self.another)

    def test_issubset_with_python_set(self):
        self.s.add('a')

        self.set = set()

        self.assertFalse(self.s <= self.set)

    def test_issubset_raise_when_other_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.another.name, 'string') 
            self.s <= self.another

    # issubset <, true subset

    def test_istruesubset_True(self):
        self.another.add('a')

        self.assertTrue(self.s < self.another)

    def test_istruesubset_False(self):
        self.s.add('a')

        self.assertFalse(self.s < self.another)

    def test_istruesubset_with_python_set(self):
        self.s.add('a')

        self.set = set()

        self.assertFalse(self.s < self.set)

    def test_istruesubset_raise_when_other_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.another.name, 'string') 
            self.s < self.another

    # superset >=

    def test_issuperset_True(self):
        self.s.add('a')

        self.assertTrue(self.s >= self.another)

    def test_issuperset_False(self):
        self.another.add('b')

        self.assertFalse(self.s >= self.another)

    def test_issuperset_with_python_set(self):
        self.s.add('a')

        self.set = set()

        self.assertTrue(self.s >= self.set)

    def test_issuperset_raise_when_other_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.another.name, 'string') 
            self.s >= self.another

    # superset >, ture super set

    def test_isturesuperset_True(self):
        self.s.add('a')
        self.s.add('b')
        
        self.another.add('a')

        self.assertTrue(self.s > self.another)

    def test_isturesuperset_False(self):
        self.s.add('a')
        self.another.add('a')

        self.assertFalse(self.s > self.another)

    def test_istruesuperset_with_python(self):
        self.s.add('a')

        self.set = set()

        self.assertTrue(self.s > self.set)

    def test_isturesuperset_raise_when_other_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.another.name, 'string')
            self.s > self.another

    # union(operator) |

    def test_op_union(self):
        self.s.add('a')
        self.another.add('b')

        self.assertEqual(self.s | self.another, {'a','b'})

    def test_op_union_with_multi_operand(self):
        self.s.add('a')
        self.another.add('b')
        self.third.add('c')

        self.assertEqual(self.s | self.another | self.third,
                         {'a', 'b', 'c'})

    def test_op_union_with_python_set(self):
        self.s.add('a')

        self.set = set('b')

        self.assertEqual(self.s | self.set, {'a', 'b'})
    
    def test_op_union_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.another.name, 'string')
            self.s | self.another

    # inser(operator) &

    def test_op_inter(self):
        self.s.add('a')

        self.another.add('a')
        self.another.add('b')

        self.assertEqual(self.s & self.another, {'a'})

    def test_op_inter_with_multi_operand(self):
        self.s.add('a')
        self.another.add('a')
        self.third.add('c')
        self.third.add('a')

        self.assertEqual(self.s & self.another & self.third,
                         {'a'})

    def test_op_inter_with_python_set(self):
        self.s.add('a')

        self.set = set('a')

        self.assertEqual(self.s & self.set, {'a'})

    def test_op_inter_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.another.name, 'string')
            self.s & self.another

    # diff(operator) -
    
    def test_op_diff(self):
        self.s.add('a')

        self.assertEqual(self.s - self.another, {'a'})

    def test_op_diff_with_multi_operand(self):
        self.s.add('a')
        self.s.add('b')
        self.s.add('c')

        self.another.add('b')

        self.third.add('c')

        self.assertEqual(self.s - self.another - self.third,
                         {'a'})

    def test_op_diff_with_python_set(self):
        self.s.add('a')

        self.set = set()

        self.assertEqual(self.s - self.set, {'a'})

    def test_op_diff_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.another.name, 'string')
            self.s - self.another

    # symmetric diff(operator) ^

    def test_op_sym_diff(self): 
        self.s.add('a')
        self.s.add('c')

        self.another.add('a')
        self.another.add('f')

        self.assertEqual(self.s ^ self.another, {'c', 'f'})

    def test_op_sym_diff_with_multi_operand(self):
        self.s.add('a')
        self.s.add('c')

        self.another.add('a')
        self.another.add('f')

        self.third.add('g')

        self.assertEqual(self.s ^ self.another ^ self.third,
                         {'c', 'f', 'g'})

    def test_op_sym_diff_with_python_set(self):
        self.s.add('a')
        self.s.add('b')

        self.set = {'a', 'c'}

        self.assertEqual(self.s ^ self.set, {'b', 'c'})

    def test_op_sym_diff_raise_when_wrong_type(self):
        with self.assertRaises(TypeError):
            self.redispy.set(self.another.name, 'string')
            self.s ^ self.another

if __name__ == "__main__":
    unittest.main()
