#! /usr/bin/env python2.7
# coding: utf-8

import unittest
import ooredis.type_case as type_case
from ooredis.type_case import *

from redis import Redis

class Person:
    """ test serialize type case """
    name = "huangz"

class TestTypeCase(unittest.TestCase):

    def setUp(self):
        r = Redis()
        r.flushdb()

    """
    GenericTypeCase
    """

    def test_generic_type_case_to_redis(self):

        # int
        self.i = GenericTypeCase.to_redis(10086)
        self.assertEqual(self.i, 10086)
        self.assertTrue(isinstance(self.i, int))

        # float
        self.f = GenericTypeCase.to_redis(3.14)
        self.assertEqual(self.f, 3.14)
        self.assertTrue(isinstance(self.f, float))

        # str
        self.s = GenericTypeCase.to_redis('hello')
        self.assertEqual(self.s, 'hello')
        self.assertTrue(isinstance(self.s, str))

        # unicode
        self.u = GenericTypeCase.to_redis(u'hello')
        self.assertEqual(self.u, u'hello')
        self.assertTrue(isinstance(self.u, unicode))

        # object
        with self.assertRaises(ValueError):
            GenericTypeCase.to_redis(Person())

    
    def test_generic_type_case_to_python(self):
        
        # str int
        self.i = GenericTypeCase.to_python(str(10086))
        self.assertEqual(self.i, 10086)
        self.assertTrue(isinstance(self.i, int))

        # str float
        self.f = GenericTypeCase.to_python(str(3.14))
        self.assertEqual(self.f, 3.14)
        self.assertTrue(isinstance(self.f, float))

        # str
        self.s = GenericTypeCase.to_python('hello')
        self.assertEqual(self.s, 'hello')
        self.assertTrue(isinstance(self.s, str))

        # unicode
        self.u = GenericTypeCase.to_python(u'hello')
        self.assertEqual(self.u, 'hello')   # str
        self.assertTrue(isinstance(self.u, str))

        # real unicode needed
        self.real_u = GenericTypeCase.to_python(u'哈哈')
        self.assertEqual(self.real_u, u'哈哈')
        self.assertTrue(isinstance(self.real_u, unicode))

    """
    IntTypeCase

    测试整数类型，包括int和long，
    还要测试float类型，防止一些不可预知的问题。
    """
        
    def test_int_type_case_to_redis(self):
        
        # int
        self.assertEqual(IntTypeCase.to_redis(10086), 10086)
        self.assertTrue(isinstance(IntTypeCase.to_redis(10086), int))

        # long
        self.assertEqual(IntTypeCase.to_redis(10086L), 10086L)
        self.assertTrue(isinstance(IntTypeCase.to_redis(10086L), long))

        # not int (float)
        with self.assertRaises(ValueError):
            IntTypeCase.to_redis(3.14)

        # not int (str)
        with self.assertRaises(ValueError):
            IntTypeCase.to_redis('hello')

    def test_int_type_case_to_python(self):
        
        # int
        self.assertEqual(IntTypeCase.to_python(str(10086)), 10086)
        self.assertTrue(isinstance(IntTypeCase.to_python(str(10086)), int))

        # long
        self.assertEqual(IntTypeCase.to_python(str(10086L)), 10086)
        self.assertTrue(isinstance(IntTypeCase.to_python(str(10086L)), int))

        # not int (float)
        with self.assertRaises(ValueError):
            IntTypeCase.to_python(str(3.14))

        # not int (str)
        with self.assertRaises(ValueError):
            IntTypeCase.to_python('hello')

    """
    FloatTypeCase

    测试浮点数，时要连int类型一起测，
    防止一些不可预计的问题。
    """
    
    def test_float_type_case_to_redis(self):
        
        # float
        self.assertEqual(FloatTypeCase.to_redis(3.14), 3.14)
        self.assertTrue(isinstance(FloatTypeCase.to_redis(3.14), float))

        # not float (int)
        with self.assertRaises(ValueError):
            FloatTypeCase.to_redis(10086)

        # not float (str)
        with self.assertRaises(ValueError):
            FloatTypeCase.to_redis('hello')

    def test_float_type_case_to_python(self):
        
        # float
        self.f  = FloatTypeCase.to_python(str(3.14))
        self.assertEqual(self.f, 3.14)
        self.assertTrue(isinstance(self.f, float))

        # not float (int)
        self.i = FloatTypeCase.to_python(str(10086))
        self.assertEqual(self.i, 10086.0)
        self.assertTrue(isinstance(self.i, float))

        # not float (str)
        with self.assertRaises(ValueError):
            FloatTypeCase.to_python('hello')

    """
    StringTypeCase

    这里字符串要分为4类来测试：
    1.ascii编码的字符
    2.unicode编码的ascii字符
    3.unicode编码的非ascii字符
    4.非字符串类型，int，float之类都可以。
    """

    def test_string_type_case_to_redis(self):

        # str
        self.s = StringTypeCase.to_redis('hello')
        self.assertEqual(self.s, 'hello')
        self.assertTrue(isinstance(self.s, str))

        # unicode
        self.u = StringTypeCase.to_redis(u'hello')
        self.assertEqual(self.u, u'hello')
        self.assertTrue(isinstance(self.u, unicode))

        # real unicode needed
        self.real_u = StringTypeCase.to_redis(u'哈哈')
        self.assertEqual(self.real_u, u'哈哈')
        self.assertTrue(isinstance(self.real_u, unicode))

        # not str (int)
        with self.assertRaises(ValueError):
            StringTypeCase.to_redis(10086)

    def test_string_type_case_to_python(self):
        
        # str
        self.s = StringTypeCase.to_python('hello')
        self.assertEqual(self.s, 'hello')
        self.assertTrue(isinstance(self.s, str))

        # unicode(ascii)
        self.u = StringTypeCase.to_python(u'hello')
        self.assertEqual(self.s, 'hello')   # still str
        self.assertTrue(isinstance(self.s, str))    # str

        # real unicode needed
        self.real_u = StringTypeCase.to_python(u'哈哈')
        self.assertEqual(self.real_u, u'哈哈')
        self.assertTrue(isinstance(self.real_u, unicode))

        # not str (int)
        self.assertEqual(StringTypeCase.to_python(10086), str(10086))


    """
    JsonTypeCase
    """

    def test_json_type_case(self):

        self.to_json = lambda value: JsonTypeCase.to_python(JsonTypeCase.to_redis(value))

        self.d = {'name': 'huangz'}

        self.assertEqual(self.to_json(self.d), self.d)
        self.assertTrue(isinstance(self.to_json(self.d), dict))

        # to_redis raise error
        with self.assertRaises(TypeError):
            JsonTypeCase.to_redis(Person())

        # out raise error
        with self.assertRaises(ValueError):
            JsonTypeCase.to_python('hello')


    """
    SerializeTypeCase
    """

    def test_serialize_type_case(self):

        self.to_object = lambda value: SerializeTypeCase.to_python(SerializeTypeCase.to_redis(value))

        self.obj = self.to_object(Person())
        
        self.assertEqual(self.obj.name, Person.name)
        self.assertTrue(isinstance(self.obj, Person))

        # to_python raise error 
        with self.assertRaises(KeyError):
            SerializeTypeCase.to_python('哈咯')
    

if __name__ == "__main__":
    unittest.main()
