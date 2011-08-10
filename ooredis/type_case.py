# coding: utf-8

__all__ = ['GenericTypeCase','IntTypeCase', 'FloatTypeCase', 'StringTypeCase', 'JsonTypeCase', 'SerializeTypeCase']

import json
import pickle

is_unicode = lambda value: isinstance(value, unicode)
is_str = lambda value: isinstance(value, str)
is_basestring = lambda value: is_unicode(value) or is_str(value) 

is_integer = lambda value: isinstance(value, int) or isinstance(value, long)
is_float = lambda value: isinstance(value, float)

class GenericTypeCase:
    """ 一般的类型转换类，可以处理str,unicode,int和float。 """

    @staticmethod
    def to_redis(value):
        """ 接受int/long/str/unicode/float类型值，
        否则抛出ValueError。
        """
        if not is_basestring(value) and \
           not is_integer(value) and \
           not is_float(value):
            raise ValueError

        return value

    @staticmethod
    def to_python(value):
        """ 将int/long/str/unicode/float转回
        原来的值，如果转换失败，抛出
        ValueError。
        """
        if value == None:
            return None

        # NOTE: 该转换的基础是在redis储存字符串
        #       的假定之下的，如果redis储存的不是
        #       字符串，该转换结果将是不准确的。
        #       比如，当Redis储存的是浮点值3.14的时候，
        #       在这里它会被转换成整数3。
        assert(isinstance(value, basestring))

        # NOTE: 在这里，unicode编码的ascii字符也会首先
        #       被转成str类型，而真正需要unicode的字符，
        #       比如unicode编码的中文，才会转换为unicode。
        #
        #       将str作为首要编码主要是兼容性
        #       上的考虑，等python3普及之后，
        #       unicode可以成为首选。
        try:
            return int(value)
        except:
            pass

        try:
            return float(value)
        except:
            pass

        try:
            return str(value)
        except:
            pass

        try:
            return unicode(value)
        except:
            pass

        raise ValueError


class IntTypeCase:
    """ 将python值转换为int(long)类型。 """

    @staticmethod
    def to_redis(value):
        """ 接受int类型值，否则抛出ValueError。 """
        if not is_integer(value):
            raise ValueError

        return value

    @staticmethod
    def to_python(value):
        """ 尝试将值转回int类型，
        如果转换失败，抛出ValueError。
        """
        if value == None:
            return None

        return int(value)


class FloatTypeCase:
    """ 将python值转换为float类型。 """

    @staticmethod
    def to_redis(value):
        """ 接受float类型值，否则抛出ValueError。 """
        if not is_float(value):
            raise ValueError

        return float(value)

    @staticmethod
    def to_python(value):
        """ 尝试将值转回float类型，
        如果转换失败，抛出ValueError。
        """
        if value == None:
            return None

        return float(value)


class StringTypeCase:
    """ 将python值转换为字符串类型(str或unicode)。 """

    @staticmethod
    def to_redis(value):
        """ 接受basestring子类的值，否则抛出ValueError。 """
        if not is_basestring(value):
            raise ValueError

        return value

    @staticmethod
    def to_python(value):
        """ 尝试将值转回str或unicode类型，
        如果转换失败，抛出ValueError。
        """
        if value == None:
            return None

        try:
            return str(value)
        except:
            pass

        try:
            return unicode(value)
        except:
            pass

        raise ValueError


class JsonTypeCase:
    """ 将python对象转化为JSON对象。 """

    @staticmethod
    def to_redis(value):
        """ 将值转成JSON对象，
        如果值不能转成JSON对象，抛出TypeError异常。
        """
        return json.dumps(value)
    
    @staticmethod
    def to_python(value):
        """ 将Json对象转回原来的类型。
        如果转换失败，抛出ValueError。
        """
        if value == None:
            return None
        return json.loads(value)


class SerializeTypeCase:
    """ 将python对象序列化(使用pickle模块)。 """

    @staticmethod
    def to_redis(value):
        """ 将值序列化(包括自定义类和Python内置类)。 """
        return pickle.dumps(value)

    @staticmethod
    def to_python(value):
        """ 将序列化的字符串转换回原来的对象，
        如果反序列化不成功，返回KeyError
        """
        if value == None:
            return None
        return pickle.loads(value)
