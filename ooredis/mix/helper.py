# coding:utf-8

__all__ = [
    'format_key',
    'get_key_name_from_list',
    'get_key_name_from_single_value', 
]
           
from ooredis.mix.key import Key

def get_key_name_from_single_value(key):
    """ 从单个值中获取key对象的名字。 """
    return key.name if isinstance(key, Key) else key
   
def get_key_name_from_list(iterable):
    """ 从列表/元组中获取多个key对象的名字。 """
    return map(get_key_name_from_single_value, iterable)

def format_key(key, name, value):
    """ 提供对 Key 对象的格式化支持。"""
    type = key.__class__.__name__.title()
    return "{0} Key '{1}': {2}".format(type, name, value)
