# coding: utf-8

from helper import is_any_instance
from numbers import Integral

class GenericTypeCase:

    """ 
    通用类型转换类，可以处理 str/unicode/int/float 类型值。
    """

    @staticmethod
    def encode(value):
        """ 
        接受 int/long/str/unicode/float 类型值，
        否则抛出 TypeError 。
        """
        if is_any_instance(value, basestring, Integral, float):
            return value

        raise TypeError

    @staticmethod
    def decode(value):
        """ 
        将传入值转换成 int/long/str/unicode/float 等格式。
        因为 redis 只返回字符串值，这个函数也只接受字符串值，
        否则抛出 TypeError 。
        """
        if value is None:
            return None
        elif not isinstance(value, basestring):
            # redis 返回的只能是字符串值
            raise TypeError
        else:
            # 从最限定的类型开始转换
            try: return int(value)
            except:
                try: return float(value)
                except:
                    try: return str(value)
                    except:
                        return unicode(value)
