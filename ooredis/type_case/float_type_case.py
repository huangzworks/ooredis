# coding: utf-8

from numbers import Integral
from helper import is_any_instance

class FloatTypeCase:

    """ 
    处理 float 类型值的转换。 
    """

    @staticmethod
    def encode(value):
        """
        接受 float 类型值，否则抛出 TypeError 。 
        """
        if is_any_instance(value, float, int):
            return float(value)
        
        raise TypeError

    @staticmethod
    def decode(value):
        """ 
        尝试将值转换成 float 类型，
        如果转换失败，抛出 TypeError 。
        """
        return None if value is None else float(value)
