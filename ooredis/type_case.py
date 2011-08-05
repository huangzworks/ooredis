# coding: utf-8

import json
import pickle


class GenericTypeCase:
    """ 一般的类型转换类，可以处理str,unicode,int和float。 """

    @staticmethod
    def to_redis(value):
        # NOTE: unicode only
        if isinstance(value, basestring):
            value = unicode(value)
        return value

    @staticmethod
    def to_python(value):
        if value == None:
            return None

        # NOTE: 该转换的基础是在redis储存字符串
        #       的假定之下的，如果redis储存的不是
        #       字符串，该转换结果将是不准确的。
        assert(isinstance(value, basestring))

        try:
            return int(value)
        except:
            pass

        try:
            return float(value)
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
        return int(value)

    @staticmethod
    def to_python(value):
        if value == None:
            return None
        return int(value)


class FloatTypeCase:
    """ 将python值转换为float类型。 """

    @staticmethod
    def to_redis(value):
        return float(value)

    @staticmethod
    def to_python(value):
        if value == None:
            return None
        return float(value)


class StringTypeCase:
    """ 将python值转换为字符串类型(unicode编码)。 """

    @staticmethod
    def to_redis(value):
        return unicode(value)

    @staticmethod
    def to_python(value):
        if value == None:
            return None
        return unicode(value)


class JsonTypeCase:
    """ 将python对象转化为JSON对象。 """

    @staticmethod
    def to_redis(value):
        return json.dumps(value)
    
    @staticmethod
    def to_python(value):
        if value == None:
            return None
        return json.loads(value)


class SerializeTypeCase:
    """ 将python对象序列化(使用pickle模块)。 """

    @staticmethod
    def to_redis(value):
        return pickle.dumps(value)

    @staticmethod
    def to_python(value):
        if value == None:
            return None
        return pickle.loads(value)
