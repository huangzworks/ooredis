# coding:utf-8

__metaclass__ = type

from ooredis.mix.key import Key

def get_key_name_from_single_value(key):
    """ 从单个值中获取key对象的名字。 """
    return key.name if isinstance(key, Key) else key
   
def get_key_name_from_list(iterable):
    """ 从列表/元组中获取多个key对象的名字。 """
    return map(get_key_name_from_single_value, iterable)
