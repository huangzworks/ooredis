# coding: utf-8

import pickle

class SerializeTypeCase:

    """ 
    处理 python 对象序列化(使用 pickle 模块)。
    """

    @staticmethod
    def encode(value):
        """ 
        将值序列化(包括自定义类和 Python 内置类)。
        如果传入的值无法被序列化，抛出 TypeError 。
        """
        try:
            return pickle.dumps(value)
        except pickle.PicklingError:
            raise TypeError

    @staticmethod
    def decode(value):
        """ 
        将序列化的字符串转换回原来的对象，
        如果传入值无法进行反序列化，抛出 TypeError 。
        """
        if value is None:
            return None

        try:
            return pickle.loads(value)
        except pickle.UnpicklingError:
            raise TypeError
