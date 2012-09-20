# coding: utf-8

__all__ = ['connect', 'get_client']

import redis

client = None

def connect(*args, **kwargs):
    """ 连接Redis数据库，参数和redis-py的Redis类一样 """
    global client
    client = redis.Redis(*args, **kwargs)

def get_client():
    """ 返回OORedis客户端 """
    global client

    if client is None:
        connect()

    return client
