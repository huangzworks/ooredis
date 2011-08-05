# coding:utf-8

__all__ = ['Dict']

__metaclass__ = type

import collections
import redis.exceptions as redispy_exception

from ooredis.const import REDIS_TYPE
from ooredis.mix.key import Key

DEFAULT_INCREMENT = DEFAULT_DECREMENT = 1

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
            TypeError: 如果传入的value不是适合的类型。
                       或key对象不是字典类型。
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
            TypeError: 如果value不是适合的类型抛出。
                       或key对象不是hash类型。
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
        如果dict[key]不存在，沉默。

        Args:
            key: 字典的键

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 当key对象不是字典类型时抛出。
        """
        try:
            self._client.hdel(self.name, key)
        except redispy_exception.ResponseError:
            raise TypeError

    def __iter__(self):
        """ 返回字典所有key。

        Time:
            O(N)

        Returns:
            iterator: 包含所有字典所有key的一个生成器。
        
        Raises:
            TypeError: 当key对象不是字典类型时抛出。
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
            TypeError: 当key对象不是hash类型时抛出。
        """
        try:
            return self._client.hlen(self.name)
        except redispy_exception.ResponseError:
            raise TypeError

    def incr(self, key, increment=DEFAULT_INCREMENT):
        """ 将dict[key]中的值加上increment。

        Args:
            key: 键
            increment：增量

        Time:
            O(1)

        Returns:
            int: 当前dict[key]中的值

        Raises:
            KeyError:如果dict[key]存在且储存的不是整数类型时抛出。
            TypeError:对非字典类型进行incr操作时抛出。
        """
        if self.exists and self._represent != REDIS_TYPE['hash']:
            raise TypeError
        try:
            return self._client.hincrby(self.name, key, increment)
        except redispy_exception.ResponseError:
            raise KeyError

    def decr(self, key, decrement=DEFAULT_DECREMENT):
        """ 将dict[key]中的值减去decrement。

        Args:
            key: 键
            decrement：减量

        Time:
            O(1)

        Returns:
            int: 当前dict[key]中的值

        Raises:
            KeyError:如果dict[key]存在且储存的不是整数类型时抛出。
            TypeError:对非字典类型进行incr操作时抛出。
        """
        return self.incr(key, 0-decrement)
