# coding: utf-8

__all__ = ['Counter']

__metaclass__ = type

from ooredis import String
from ooredis.type_case import IntTypeCase
from ooredis.key.helper import wrap_exception
from ooredis.const import DEFAULT_INCREMENT, DEFAULT_DECREMENT

class Counter(String):

    """
    计算器用途的 key 对象。
   
    注意当 Key 对象为空时，get/getset 的返回值为 None。
    """

    def __init__(self, name, client=None, type_case=IntTypeCase):
        """ 
        初始化一个 Counter 类实例，
        使用 IntTypeCase 作为默认 type case 。
        """
        super(Counter, self).__init__(name=name, client=client, type_case=type_case)


    @wrap_exception
    def incr(self, increment=DEFAULT_INCREMENT):
        """
        将计数器的值加上增量 increment， 
        然后返回执行 incr 操作之后计数器的当前值。

        Args:
            increment: 增量，默认为 1 。

        Time:
            O(1)

        Returns:
            current_counter_value

        Raises:
            TypeError: 当 Key 对象储存的不是数值类型时抛出。
        """
        # redis-py用incr代替redis的incrby
        return self._client.incr(self.name, increment)


    @wrap_exception
    def decr(self, decrement=DEFAULT_DECREMENT):
        """
        将计数器的值减去减量 decrement ，
        然后返回执行 decr 操作之后计数器的当前值。

        Args:
            decrement: 减量，默认为1.

        Time:
            O(1)

        Returns:
            current_counter_value

        Raises:
            TypeError: 当 key 储存的不是数值类型时抛出。
        """
        # redis-py用decr代替redis的decrby
        return self._client.decr(self.name, decrement)


    def __iadd__(self, increment):
        """
        self.incr 方法的一个 python 语法糖，
        区别是这个特殊方法不返回 key 对象的当前值。

        Args:
            increment: 增量。

        Time:
            O(1)

        Returns:
            self: python 要求这个特殊方法返回被修改后的对象。

        Raises:
            TypeError: 当 key 储存的不是数值类型时由 self.incr 抛出。
        """
        self.incr(increment)
        return self


    def __isub__(self, decrement):
        """
        self.decr 方法的一个 python 语法糖，
        区别是这个特殊方法不返回 key 对象的当前值。

        Args:
            decrement: 减量。

        Time:
            O(1)

        Returns:
            self: python 要求这个特殊方法返回被修改后的对象。

        Raises:
            TypeError: 当 key 储存的不是数值类型时由 self.decr 抛出。
        """
        self.decr(decrement)
        return self
