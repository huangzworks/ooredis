# coding: utf-8

__all__ = ['connect', 'get_client']

__metaclass__ = type

import redis

__client = None

def connect(*args, **kwargs):
    """ 连接Redis数据库，参数和redis-py的Redis类一样 """
    global __client
    __client = redis.Redis(*args, **kwargs)

def get_client():
    """ 返回OORedis客户端 """
    global __client

    if __client == None:
        __client = redis.Redis()

    return __client
