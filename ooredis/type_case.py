# coding: utf-8

__all__ = [
    'GenericTypeCase','IntTypeCase', 'FloatTypeCase',
    'StringTypeCase','JsonTypeCase', 'SerializeTypeCase'
]

__metaclass__ = type

import json
import pickle

from numbers import Integral

# helper
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def accept_type(*types):
    """ 接受一个类型列表，返回一个匿名函数。
    匿名函数接受一个值，如果值的类型不是类型列表的其中一个，
    那么返回 False。
    """
    return lambda value: any(map(lambda t: isinstance(value, t), types))


# type case class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GenericTypeCase:

    """ 通用类型转换类，可以处理 str/unicode/int/float 类型值。 """

    @staticmethod
    def to_redis(value):
        """ 接受 int/long/str/unicode/float 类型值，
        否则抛出 ValueError。
        """
        if not accept_type(basestring, Integral, float)(value):
            raise ValueError

        return value

    @staticmethod
    def to_python(value):
        """ 将 int/long/str/unicode/float 转回原来的值，
        如果转换失败，抛出 ValueError 。
        """
        if value is None:
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
            try: 
                return float(value)
            except:
                try:
                    return str(value)
                except:
                    try: 
                        return unicode(value)
                    except:
                        raise ValueError


class IntTypeCase:

    """ 处理 int(long) 类型值的转换。 """

    @staticmethod
    def to_redis(value):
        """ 接受 int 类型值，否则抛出 ValueError。 """
        if not accept_type(Integral)(value):
            raise ValueError

        return value

    @staticmethod
    def to_python(value):
        """ 尝试将值转回 int 类型，
        如果转换失败，抛出 ValueError。
        """
        if value is None:
            return None

        return int(value)


class FloatTypeCase:

    """ 处理 float 类型值的转换。 """

    @staticmethod
    def to_redis(value):
        """ 接受 float 类型值，否则抛出 ValueError。 """
        if not accept_type(float)(value):
            raise ValueError

        return float(value)

    @staticmethod
    def to_python(value):
        """ 尝试将值转回 float 类型，
        如果转换失败，抛出 ValueError 。
        """
        if value is None:
            return None

        return float(value)


class StringTypeCase:

    """ 处理字符串类型(str或unicode)值的转换。 """

    @staticmethod
    def to_redis(value):
        """ 接受 basestring 子类的值(str或unicode)，
        否则抛出ValueError。
        """
        if not accept_type(basestring)(value):
            raise ValueError

        return value

    @staticmethod
    def to_python(value):
        """ 尝试将值转回str或unicode类型，
        如果转换失败，抛出ValueError。
        """
        if value is None:
            return None

        try:
            return str(value)
        except:
            try:
                return unicode(value)
            except:
                raise ValueError


class JsonTypeCase:

    """ 将 python 对象转化为 JSON 对象。 """

    @staticmethod
    def to_redis(value):
        """ 将值转成 JSON 对象，
        如果值不能转成 JSON 对象，抛出 TypeError 异常。
        """
        return json.dumps(value)
    
    @staticmethod
    def to_python(value):
        """ 将 Json 对象转回原来的类型。
        如果转换失败，抛出 ValueError 。
        """
        if value is None:
            return None

        return json.loads(value)


class SerializeTypeCase:

    """ 将 python 对象序列化(使用 pickle 模块)。 """

    @staticmethod
    def to_redis(value):
        """ 将值序列化(包括自定义类和 Python 内置类)。 """
        return pickle.dumps(value)

    @staticmethod
    def to_python(value):
        """ 将序列化的字符串转换回原来的对象，
        如果反序列化不成功，返回 KeyError
        """
        if value is None:
            return None

        return pickle.loads(value)
