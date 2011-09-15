# coding: utf-8

__all__ = ['connect', 'get_client']

__metaclass__ = type

import redis

class SingletonClientMeta(type):
    
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance == None:
            cls._instance = redis.Redis(*args, **kwargs)
        return cls._instance

class Redis:
    
    __metaclass__ = SingletonClientMeta


# helper functions:

def connect(*args, **kwargs):
    return Redis(*args, **kwargs)

def get_client():
    return Redis()
