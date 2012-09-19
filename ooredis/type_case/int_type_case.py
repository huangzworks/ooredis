# coding: utf-8

from numbers import Integral

class IntTypeCase:

    """ 
    处理 int(long) 类型值的转换。
    """

    @staticmethod
    def encode(value):
        """ 
        接受 int 类型值，否则抛出 TypeError 。 
        """
        if isinstance(value, Integral):
            return value

        raise TypeError

    @staticmethod
    def decode(value):
        """ 
        尝试将值转回 int 类型，
        如果转换失败，抛出 TypeError。
        """
        if value is None:
            return None
        else:
            try:
                return int(value)
            except:
                try:
                    return long(value)
                except:
                    raise TypeError
