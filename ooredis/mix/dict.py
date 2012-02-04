# coding:utf-8

__all__ = ['Dict']

__metaclass__ = type

import collections
import redis.exceptions as redispy_exception

from ooredis.mix.key import Key
from ooredis.const import REDIS_TYPE

KEY_NOT_IN_DICT_AND_DELETE_FALSE = False

class Dict(Key, collections.MutableMapping):

    """ 一个字典对象，底层是redis的hash实现。 """

    def __repr__(self):
        # TODO: key_values 未转义
        key_type = self.__class__.__name__.title()
        key_name = self.name
        key_values = dict(self.items())
        return "{0} Key '{1}': {2}".format(key_type, key_name, key_values)

    def __setitem__(self, key, python_value):
        """ 
        将字典中键 key 的值设为 value 。
        如果键 key 已经关联了另一个值 ，那么将它覆盖。

        Args:
            key
            python_value

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: Key 对象不是 Dict 类型时抛出。
        """
        try:
            redis_value = self._type_case.to_redis(python_value)
            self._client.hset(self.name, key, redis_value)
        except redispy_exception.ResponseError:
            raise TypeError

    def __getitem__(self, key):
        """ 
        返回字典中键 key 的值。
        如果键 key 的值不存在，那么抛出 KeyError 。

        Args:
            key

        Time:
            O(1)

        Returns:
            python_value

        Raises:
            KeyError: key 不存在时抛出。
            TypeError: Key 对象不是 Dict 类型时抛出。
        """
        # 将 TypeError 的抛出单独抽取出来
        # 让 MIXIN 方法的行为和 Python dict 类保持一致。
        if self.exists and self._represent != REDIS_TYPE['hash']:
            raise TypeError

        # 没有自己实现 __contains__ 的话
        # 不要使用 key in self ，否则将引起死循环
        if not self._client.hexists(self.name, key):
            raise KeyError

        redis_value = self._client.hget(self.name, key)
        python_value = self._type_case.to_python(redis_value)

        return python_value

    def __delitem__(self, key):
        """ 
        删除字典键 key 的值。
        如果键 key 的值不存在，那么抛出 KeyError 。

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
        """ 
        返回一个包含字典里所有键的迭代器。

        Args:
            None

        Time:
            O(N)

        Returns:
            iterator
        
        Raises:
            TypeError: Key 对象不是 Dict 类型时抛出。
        """
        try:
            for key in self._client.hkeys(self.name):
                yield key
        except redispy_exception.ResponseError:
            raise TypeError

    def __len__(self):
        """
        返回字典中键-值对的个数。
        空字典返回 0 。

        Args:
            None

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
