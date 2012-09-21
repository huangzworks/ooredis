# coding: utf-8

class StringTypeCase:

    """ 
    处理字符串类型( str 或 unicode )值的转换。 
    """

    @staticmethod
    def encode(value):
        """ 
        接受 basestring 子类的值( str 或 unicode )，
        否则抛出 TypeError 。
        """
        if isinstance(value, basestring):
            return value

        raise TypeError

    @staticmethod
    def decode(value):
        """ 
        将值转回 str 或 unicode 类型。 
        """
        if value is None:
            return 

        try:
            return str(value)
        except:
            return unicode(value)
