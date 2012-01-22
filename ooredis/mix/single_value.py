# coding: utf-8

__all__ = ['SingleValue', 'Counter']

__metaclass__ = type

import redis.exceptions as redispy_exception

from ooredis.mix.key import Key
from ooredis.const import REDIS_TYPE

class SingleValue(Key):
    """ 为储存单个值的 key 对象提供 set，get，getset操作。 """

    def __repr__(self):
        key_type = self.__class__.__name__.title()
        key_name = self.name
        key_value = self.get()
        return "{0} Key '{1}': {2}".format(key_type, key_name, key_value)

    def set(self, python_value, preserve=False, expire=None):
        """ 为 key 对象指定一个值。

        Args:
            python_value: 值。
            preserve: 指定是否不覆盖原本储存的值。
            expire: 设置 key 的过期时间，以秒为单位。

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 当 key 非空且 key 不是指定类型时抛出。
            ValueError: 根据 preserve 参数的情况抛出。
        """
        # NOTE:
        # set 命令可以无视类型进行设置的命令。
        # 为了保证类型的限制，
        # ooredis 里对一个非字符串类型进行 set 将引发 TypeError 异常。
        if self.exists and self._represent != REDIS_TYPE['string']:
                raise TypeError

        if self.exists and preserve:
            raise ValueError
       
        redis_value = self._type_case.to_redis(python_value)
        if expire:
            self._client.setex(self.name, redis_value, expire)
        else:
            self._client.set(self.name, redis_value)

    def get(self):
        """ 返回 key 对象的值。

        Time:
            O(1)

        Returns:
            value： key 的值。
            None: key 不存在时返回。

        Raises:
            TypeError: 当 key 非空且不是 string 类型时抛出。
        """
        try:
            redis_value = self._client.get(self.name)
            return self._type_case.to_python(redis_value)
        except redispy_exception.ResponseError:
            raise TypeError

    def getset(self, python_value):
        """ 修改 key 的值，并返回 key 之前的值。

        Args:
            value: key 对象的新值。

        Time:
            O(1)

        Returns:
            None: 当 key 不存时(没有前值)返回。
            value: 否则，返回 key 之前的值。

        Raises:
            TypeError: 当 key 非空且不是 string 类型时抛出。
        """
        try:
            new_redis_value = self._type_case.to_redis(python_value)
            original_redis_value = self._client.getset(self.name, new_redis_value)

            return self._type_case.to_python(original_redis_value)
        except redispy_exception.ResponseError:
            raise TypeError


class Counter(SingleValue):
    """
    为计数类型的 key 对象加上 incr ，
    decr 以及 += 和 -= 方法。
    """

    def incr(self, increment=1):
        """
        将 key 对象的值加上增量 increment， 
        然后返回执行加法之后 key 对象的值。

        Args:
            increment: 增量，默认为 1 。

        Time:
            O(1)

        Returns:
            int: 操作执行之后的值。

        Raises:
            TypeError: 当 key 储存的不是数值类型时抛出。
        """
        # NOTE: redis-py用incr代替redis的incrby
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
        # NOTE: redis-py用decr代替redis的decrby
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
