#! /usr/bin/env python2.7
# coding: utf-8

import unittest
import ooredis.type_case as type_case

class Person:
    """ test serialize type case """
    name = "huangz"

class TestTypeCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_generic_type_case_to_redis(self):
        generic_in = type_case.GenericTypeCase.to_redis

        self.i = generic_in(3)
        self.assertTrue(isinstance(self.i, int))
        self.assertEqual(self.i, 3)

        self.f = generic_in(3.14)
        self.assertTrue(isinstance(self.f, float))
        self.assertEqual(self.f, 3.14)

        self.s = generic_in('hi')
        self.assertTrue(isinstance(self.s, unicode))
        self.assertEqual(self.s, unicode('hi'))

        self.u = generic_in(u'hello')
        self.assertTrue(isinstance(self.u, unicode))
        self.assertEqual(self.u, u'hello')

    def test_generic_type_case_to_python(self):
        generic_out = type_case.GenericTypeCase.to_python

        self.i = generic_out('3')
        self.assertTrue(isinstance(self.i, int))
        self.assertEqual(self.i, 3)

        self.f = generic_out('3.14')
        self.assertTrue(isinstance(self.f, float))
        self.assertEqual(self.f, 3.14)

        self.s = generic_out('hi')
        self.assertTrue(isinstance(self.s, unicode))
        self.assertEqual(self.s, u'hi')

        self.u = generic_out(u'hello')
        self.assertTrue(isinstance(self.u, unicode))
        self.assertEqual(self.u, u'hello')

    def test_json_type_case(self):
        json_in = type_case.JsonTypeCase.to_redis
        json_out = type_case.JsonTypeCase.to_python

        self.dict = {'name': 'huangz', 'age':20}
        self.assertEqual(json_out(json_in(self.dict)),
                         self.dict)

    def test_int_type_case(self):
        int_in = type_case.IntTypeCase.to_redis
        int_out = type_case.IntTypeCase.to_python

        # str
        self.assertEqual(int_out(int_in('3')), 3)

        # int
        self.assertEqual(int_out(int_in(3)), 3)

        # float
        self.assertEqual(int_out(int_in(3.14)), 3)

        # unknow
        with self.assertRaises(ValueError):
            int_in('3.14')

    def test_float_type_case(self):
        float_in = type_case.FloatTypeCase.to_redis
        float_out = type_case.FloatTypeCase.to_python

        # str
        self.assertEqual(float_out(float_in('3.14')), 3.14)
        
        # int
        self.assertEqual(float_out(float_in(3)), 3.0)

        # float
        self.assertEqual(float_out(float_in(3.14)), 3.14)

        # unknow
        with self.assertRaises(ValueError):
            float_in('hello')

    def test_string_type_case(self):
        string_in = type_case.StringTypeCase.to_redis
        string_out = type_case.StringTypeCase.to_python

        # str
        self.assertEqual(string_out(string_in('hello')), u'hello')

        # int
        self.assertEqual(string_out(string_in(3)), u'3')

        # float
        self.assertEqual(string_out(string_in(3.14)), u'3.14')

    def test_serialize_type_case(self):
        obj = Person()

        serialize_in = type_case.SerializeTypeCase.to_redis
        serialize_out = type_case.SerializeTypeCase.to_python

        # str
        out = serialize_out(serialize_in(obj))
        self.assertTrue(isinstance(out, Person))
        self.assertEqual(out.name, obj.name)

if __name__ == "__main__":
    unittest.main()
