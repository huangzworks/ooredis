# coding:utf-8

__all__ = ['Dict']

__metaclass__ = type

import collections
import redis.exceptions as redispy_exception

from ooredis.mix.key import Key
from ooredis.const import (
    REDIS_TYPE,
    DEFAULT_INCREMENT,
    DEFAULT_DECREMENT,
)

KEY_NOT_IN_DICT_AND_DELETE_FALSE = False

class Dict(Key, collections.MutableMapping):
    """ 一个字典对象，底层是redis的hash实现。 """

    def __repr__(self):
        key_type = self.__class__.__name__.title()
        key_name = self.name
        key_values = dict(self.items())
        return "{0} Key '{1}': {2}".format(key_type, key_name, key_values)

    def __setitem__(self, key, value):
        """ 将dict[key]的值设为value。
        如果dict[key]已经存在，则将其覆盖。

        Args:
            key: 字典的键
            value: 字典的值

        Time:
            O(1)

        Returns:
            None

        Raises:
            ValueError: 传入的value不是合适的类型时抛出。
            TypeError: Key对象不是Dict类型时抛出。
        """
        try:
            value = self._type_case.to_redis(value)
            self._client.hset(self.name, key, value)
        except redispy_exception.ResponseError:
            raise TypeError

    def __getitem__(self, key):
        """ 返回dict[key]的值。
        如果dict[key]不存在，抛出KeyError。

        Args:
            key: 字典的键

        Time:
            O(1)

        Returns:
            value: dict[key]的值

        Raises:
            KeyError: key不存在时抛出。
            ValueError: 传入的value不是合适的类型时抛出。
            TypeError: Key对象不是Dict类型时抛出。
        """
        # NOTE: 将TypeError的抛出单独抽取出来，
        #       是为了让MIXIN方法的行为和python一致。
        if self.exists and self._represent != REDIS_TYPE['hash']:
            raise TypeError

        # WARNING: 不要在这里使用key in self语句，
        #          除非你自己实现了__contains__方法，
        #          否则迎接你的将是一个无限递归。。。
        if self._client.hexists(self.name, key) is False:
            raise KeyError

        value = self._client.hget(self.name, key)
        return self._type_case.to_python(value)

    def __delitem__(self, key):
        """ 删除dict[key]。
        如果dict[key]不存在，抛出KeyError。

        Args:
            key: 字典的键

        Time:
            O(1)

        Returns:
            None

        Raises:
            KeyError: key不存在时抛出。
            TypeError: Key对象不是Dict类型时抛出。
        """
        try:
            status = self._client.hdel(self.name, key)
            if status == KEY_NOT_IN_DICT_AND_DELETE_FALSE:
                raise KeyError
        except redispy_exception.ResponseError:
            raise TypeError

    def __iter__(self):
        """ 返回字典所有key。

        Time:
            O(N)

        Returns:
            iterator: 包含所有字典所有key的一个迭代器。
        
        Raises:
            TypeError: Key对象不是Dict类型时抛出。
        """
        try:
            for key in self._client.hkeys(self.name):
                yield key
        except redispy_exception.ResponseError:
            raise TypeError

    def __len__(self):
        """ 返回字典key-value对的个数，空字典返回0。

        Time:
            O(1)

        Returns:
            int: 字典中key-value对的个数。

        Raises:
            TypeError: Key对象不是Dict类型时抛出。
        """
        try:
            return self._client.hlen(self.name)
        except redispy_exception.ResponseError:
            raise TypeError
