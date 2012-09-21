# coding: utf-8

class FloatTypeCase:

    """ 
    处理 float 类型值的转换。 
    """

    @staticmethod
    def encode(value):
        """
        尝试将输入值转换成 float 类型，
        如果转换失败，抛出 TypeError 。
        """
        return float(value)

    @staticmethod
    def decode(value):
        """ 
        尝试将输入值转换成 float 类型，
        如果转换失败，抛出 TypeError 。
        """
        if value is not None:
            return float(value)
