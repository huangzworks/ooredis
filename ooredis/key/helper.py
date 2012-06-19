# coding:utf-8

__all__ = [
    'format_key',
    'raise_when_wrong_type',
]

import redis

from functools import wraps

def format_key(key, name, value):
    """ 
    提供对 Key 对象的格式化支持。
    """
    type = key.__class__.__name__.title()
    return "{0} Key '{1}': {2}".format(type, name, value)

def raise_when_wrong_type(func):
    """
    将 redis-py 抛出的 ResponseError 转换为 TypeError 
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except redis.exceptions.ResponseError:
            raise TypeError
    return wrapper
