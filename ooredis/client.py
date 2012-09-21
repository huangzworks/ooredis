# coding: utf-8

__all__ = ['connect', 'get_client']

import redis

client = None

def connect(*args, **kwargs):
    """ 
    连接 Redis 数据库，参数和 redis-py 的 Redis 类一样。
    """
    global client
    client = redis.Redis(*args, **kwargs)

def get_client():
    """ 
    返回 OORedis 客户端。
    """
    global client

    if client is None: connect()

    return client
