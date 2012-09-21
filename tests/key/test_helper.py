# coding:utf-8

import redis
import unittest

from ooredis.key.base_key import BaseKey
from ooredis.key.helper import format_key, wrap_exception

class TestHelper(unittest.TestCase):

    def setUp(self):
        self.name = "name"
        self.value = "value"
        self.key = BaseKey(self.name)


    # format_key

    def test_format_key(self):
        output = format_key(self.key, self.name, self.value)
        self.assertEqual( output,"Basekey Key 'name': value")

    
    # wrap_exception

    def test_wrap_exception_RAISE_TYPE_ERROR_when_ERROR_OCCUR(self):

        @wrap_exception
        def r():
            raise redis.exceptions.ResponseError

        with self.assertRaises(TypeError):
            r() 

    def test_wrap_exception_NOT_RAISE_when_NO_ERROR_OCCUR(self):

        @wrap_exception
        def f():
            return 10

        self.assertEqual(
            f(),
            10
        )


if __name__ == "__main__":
    unittest.main()
