# coding: utf-8

__all__ = ['Counter']

__metaclass__ = type

import redis.exceptions as redispy_exception
from ooredis.mix.single_value import SingleValue

class Counter(SingleValue):
    """
    为计数器类型的 Key 对象加上 incr ，decr 以及 += 和 -= 方法。
   
    注意当 Key 对象为空时，get/getset 的返回值为 None。
    """

    def incr(self, increment=1):
        """
        将 Key 对象的值加上增量 increment， 
        然后返回执行加法之后 Key 对象的值。

        Args:
            increment: 增量，默认为 1 。

        Time:
            O(1)

        Returns:
            int: 操作执行之后的值。

        Raises:
            TypeError: 当 Key 对象储存的不是数值类型时抛出。
        """
        # redis-py用incr代替redis的incrby
        try:
            return self._client.incr(self.name, increment)
        except redispy_exception.ResponseError:
            raise TypeError

    def decr(self, decrement=1):
        """
        将 key 对象的值减去减量 decrement 。
        并返回执行减法之后 key 对象的值。

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
        """
        SingleValue.incr 方法的一个 python 语法糖，
        区别是这个特殊方法不返回 key 对象的值。

        Args:
            increment: 增量。

        Time:
            O(1)

        Returns:
            self: python 要求这个特殊方法返回被修改后的对象。

        Raises:
            TypeError: 当 key 储存的不是数值类型时由 SingleValue.incr 抛出。
        """
        self.incr(increment)
        return self

    def __isub__(self, decrement):
        """
        SingleValue.decr 方法的一个 python 语法糖，
        区别是这个特殊方法不返回 key 对象的当前值。

        Args:
            decrement: 减量。

        Time:
            O(1)

        Returns:
            self: python 要求这个特殊方法返回被修改后的对象。

        Raises:
            TypeError: 当 key 储存的不是数值类型时由 SingleValue.decr 抛出。
        """
        self.decr(decrement)
        return self
