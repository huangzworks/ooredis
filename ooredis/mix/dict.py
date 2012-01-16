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
        # TODO: key_values 未转义
        key_type = self.__class__.__name__.title()
        key_name = self.name
        key_values = dict(self.items())
        return "{0} Key '{1}': {2}".format(key_type, key_name, key_values)

    def __setitem__(self, key, value):
        """ 将 self[key] 的值设为 value 。
        如果 self[key] 已经存在，则将其覆盖。

        Args:
            key
            value

        Time:
            O(1)

        Returns:
            None

        Raises:
            ValueError: 传入的 value 不是合适的类型时抛出。
            TypeError: Key 对象不是 Dict 类型时抛出。
        """
        try:
            cased_value = self._type_case.to_redis(value)
            self._client.hset(self.name, key, cased_value)
        except redispy_exception.ResponseError:
            raise TypeError

    def __getitem__(self, key):
        """ 返回 self[key] 的值。
        如果 self[key] 不存在，抛出 KeyError 。

        Args:
            key

        Time:
            O(1)

        Returns:
            value: self[key] 的值

        Raises:
            KeyError: key 不存在时抛出。
            TypeError: Key 对象不是 Dict 类型时抛出。
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

        cased_value = self._client.hget(self.name, key)
        original_value = self._type_case.to_python(cased_value)

        return original_value

    def __delitem__(self, key):
        """ 删除 self[key] 。
        如果 self[key] 不存在，抛出KeyError。

        Args:
            key

        Time:
            O(1)

        Returns:
            None

        Raises:
            KeyError: key 不存在时抛出。
            TypeError: Key 对象不是 Dict 类型时抛出。
        """
        try:
            status = self._client.hdel(self.name, key)
            if status == KEY_NOT_IN_DICT_AND_DELETE_FALSE:
                raise KeyError
        except redispy_exception.ResponseError:
            raise TypeError

    def __iter__(self):
        """ 返回 self 中所有 key 。

        Args:
            None

        Time:
            O(N)

        Returns:
            iterator: 包含所有 key 的一个迭代器。
        
        Raises:
            TypeError: Key 对象不是 Dict 类型时抛出。
        """
        try:
            for key in self._client.hkeys(self.name):
                yield key
        except redispy_exception.ResponseError:
            raise TypeError

    def __len__(self):
        """ 返回字典 key-value 对的个数，空字典返回 0 。

        Time:
            O(1)

        Returns:
            int: 字典中 key-value 对的个数。

        Raises:
            TypeError: Key 对象不是 Dict 类型时抛出。
        """
        try:
            return self._client.hlen(self.name)
        except redispy_exception.ResponseError:
            raise TypeError
