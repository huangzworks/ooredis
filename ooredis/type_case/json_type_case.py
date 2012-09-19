# coding: utf-8

import json

class JsonTypeCase:

    """ 
    用于将 python 对象转化为 JSON 对象。 
    """

    @staticmethod
    def encode(value):
        """ 
        将值转成 JSON 对象，
        如果值不能转成 JSON 对象，抛出 TypeError 异常。
        """
        return json.dumps(value)
    
    @staticmethod
    def decode(value):
        """ 
        将 Json 对象转回原来的类型。
        如果转换失败，抛出 TypeError 。
        """
        if value is None:
            return None

        return json.loads(value)
