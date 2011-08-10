# coding:utf-8

__all__ = ['Mutable', 'Counter']

__metaclass__ = type

import collections
import redis.exceptions as redispy_exception

from ooredis.const import REDIS_TYPE
from ooredis.mix.key import Key

class SingleValue(Key):
    """ 为key对象提供set，get，getset操作。 """

    def __repr__(self):
        key_type = self.__class__.__name__.title()
        key_name = self.name
        key_value = self.get()
        return "{0} Key '{1}': {2}".format(key_type, key_name, key_value)

    def set(self, value, preserve=False, expire=None):
        """ 将key对象的值改为value。

        Args:
            preserve: 指定是否不覆盖存在值。
            expire: 设置key的过期时间，以秒为单位。

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 当key非空且key不是指定类型时抛出。
            ValueError: 根据preserve参数的情况抛出。
        """
        # set命令可以无视类型进行设置的命令。
        # 为了保证类型的限制，
        # ooredis里对一个非字符串类型进行set将引发TypeError异常。
        if self.exists:
            if self._represent != REDIS_TYPE['string']:
                raise TypeError
            if preserve:
                raise ValueError
        
        value = self._type_case.to_redis(value)
        if expire:
            self._client.setex(self.name, value, expire)
        else:
            self._client.set(self.name, value)

    def get(self):
        """ 返回key对象的值。

        Time:
            O(1)

        Returns:
            value： key的值。
            None: key不存在时返回。

        Raises:
            TypeError: 当key非空且不是string类型时抛出。
        """
        try:
            value = self._client.get(self.name)
            return self._type_case.to_python(value)
        except redispy_exception.ResponseError:
            raise TypeError

    def getset(self, value):
        """ 修改key的值，并返回key之前的值。

        Args:
            value: key对象的新值。

        Time:
            O(1)

        Returns:
            None: 当key不存时(没有前值)返回。
            value: 否则，返回key之前的值。

        Raises:
            TypeError: 当key非空且不是string类型时抛出。
        """
        try:
            value = self._type_case.to_redis(value)
            old = self._client.getset(self.name, value)
            return self._type_case.to_python(old)
        except redispy_exception.ResponseError:
            raise TypeError


class Counter(SingleValue):
    """ 为数值类型的key对象加上incr，decr以及+= 和-= 语法糖。 """

    def incr(self, increment=1):
        """ 将key对象的值加上增量increment。

        Args:
            increment: 增量，默认为1.

        Time:
            O(1)

        Returns:
            int: 操作执行之后的值。

        Raises:
            TypeError: 当key储存的不是数值类型时抛出。
        """
        # redis-py用incr代替redis的incrby
        try:
            return self._client.incr(self.name, increment)
        except redispy_exception.ResponseError:
            raise TypeError

    def decr(self, decrement=1):
        """ 将key对象的值减去减量decrement。

        Args:
            decrement: 减量，默认为1.

        Time:
            O(1)

        Returns:
            int: 操作执行之后的值。

        Raises:
            TypeError: 当key储存的不是数值类型时抛出。
        """
        # redis-py用decr代替redis的decrby
        try:
            return self._client.decr(self.name, decrement)
        except redispy_exception.ResponseError:
            raise TypeError

    def __iadd__(self, increment):
        """ self.incr方法的一个python语法糖。

        和self.incr的区别是，这个特殊方法不返回key值。

        Args:
            increment: 增量。

        Time:
            O(1)

        Returns:
            self: python要求这个特殊方法返回被修改后的对象。

        Raises:
            TypeError: 当key储存的不是数值类型时由self.incr抛出。
        """
        self.incr(increment)
        return self

    def __isub__(self, decrement):
        """ self.decr方法的一个python语法糖。

        和self.decr的区别是，这个特殊方法不返回key的值。

        Args:
            decrement: 减量。

        Time:
            O(1)

        Returns:
            self: python要求这个特殊方法返回被修改后的对象。

        Raises:
            TypeError: 当key储存的不是数值类型时由self.decr抛出。
        """
        self.decr(decrement)
        return self
