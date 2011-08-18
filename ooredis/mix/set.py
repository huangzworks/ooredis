# coding:utf-8

__all__ = ['Set']

__metaclass__ = type

import collections
import redis.exceptions as redispy_exception

from ooredis.const import REDIS_TYPE
from ooredis.mix.key import (
    Key,
    get_key_name_from_single_value,
)

MEMBER_NOT_IN_SET_AND_MOVE_FALSE = 0

def get_members(set_or_set_object):
    """ 从集合对象或集合中提取成员。 """
    return set(set_or_set_object)

class Set(Key):
    """ 集合类型，底层实现是redis的set类型。 """

    def __repr__(self):
        key_type = self.__class__.__name__.title()
        key_name = self.name
        key_values = set(self)
        return "{0} Key '{1}': {2}".format(key_type, key_name, key_values)

    def __len__(self):
        """ 返回集合的基数。

        Time:
            O(1)

        Returns:
            int: 集合的基数。

        Raises:
            TypeError: 当key不是集合类型时抛出。
        """
        try:
            return self._client.scard(self.name)
        except redispy_exception.ResponseError:
            raise TypeError

    def __iter__(self):
        """ 返回集合的可迭代版本。

        Time:
            O(N)

        Returns:
            generator: 一个包含集合所有成员的迭代器。

        Raises:
            TypeError: 当key不是集合类型时抛出。
        """
        try:
            for member in self._client.smembers(self.name):
                yield self._type_case.to_python(member)
        except redispy_exception.ResponseError:
            raise TypeError

    def __contains__(self, element):
        """ 查元素element是否是集合的成员。

        Args:
            element

        Time:
            O(1)

        Returns:
            bool: element是集合成员的话True，否则False。

        Raises:
            TypeError: 当key不是集合类型时抛出。
        """
        try:
            element = self._type_case.to_redis(element)
            return self._client.sismember(self.name, element)
        except redispy_exception.ResponseError:
            raise TypeError

    def add(self, element):
        """ 将element加入到集合当中。

        如果element已经是集合的成员，不做动作。
        如果key不存在，一个空集合被创建并执行add动作。

        Args:
            element: 要加入到集合的元素

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 当key非空且key不是集合类型时抛出。
        """
        # TODO: redis2.3，add支持多个element加入。
        try:
            element = self._type_case.to_redis(element)
            self._client.sadd(self.name, element)
        except redispy_exception.ResponseError:
            raise TypeError

    def remove(self, element, check=False):
        """ 如果element是集合的成员，移除它。

        如果element不是集合成员且check为False，返回。
        如果element不是集合成员且check为True，抛出KeyError。

        Args：
            element：要删除的成员。
            check：是否检查element是否存在。

        Time：
            O(1)

        Returns:
            None

        Raises:
            TypeError: 当key非空且key不是集合类型时抛出。
            KeyError： check为True且element不是集合成员时抛出。
        """
        try:
            element = self._type_case.to_redis(element)
            delete_success = self._client.srem(self.name, element)
            if not delete_success and check:
                raise KeyError
        except redispy_exception.ResponseError:
            raise TypeError

    def pop(self):
        """ 移除并返回集合中任意一个成员。

        如果集合为空，抛出KeyError。

        Time：
            O(1)

        Returns:
            member: 集合成员。 

        Raises:
            TypeError: 当key非空且key不是集合类型时由抛出。
            KeyError: 集合为空时抛出。
        """
        try:
            element = self._client.spop(self.name)
            if element != None:
                return self._type_case.to_python(element)
            else:
                raise KeyError
        except redispy_exception.ResponseError:
            raise TypeError

    def random(self):
        """ 返回集合中的一个随机元素。

        该操作和pop相似，但pop将随机元素从集合中移除并返回，
        而random则仅仅返回随机元素，而不对集合进行任何改动。

        Time:
            O(1)

        Returns:
            member: 当集合不为空时，返回一个成员。
            None: 当集合为空时，返回None。

        Raises:
            TypeError: 当key非空且key不是集合类型时抛出。
        """
        try:
            element = self._client.srandmember(self.name)
            return self._type_case.to_python(element)
        except redispy_exception.ResponseError:
            raise TypeError

    def move(self, destination, member):
        """ 将集合成员member移动到集合destination中去。

        具体参考Redis命令：SMOVE。

        Args:
            destination: 目的地集合，可以是集合的名字(字符串)，
                         也可以是一个集合key对象。
            member: 要移动的源集合的成员。

        Time:
            O(1)

        Returns:
            None

        Raises:
            KeyError: member不存在于集合时抛出。
            TypeError: 当key非空且key不是集合类型时抛出。
        """
        try:
            destination = get_key_name_from_single_value(destination)
            member = self._type_case.to_redis(member)

            if self._client.smove(self.name, destination, member) == \
               MEMBER_NOT_IN_SET_AND_MOVE_FALSE:
                raise KeyError
        except redispy_exception.ResponseError:
            raise TypeError

    def isdisjoint(self, other):
        """ 检查集合是否和另一个集合不相交。

        Args:
            other: 一个python集合或集合key对象。
        
        Returns:
            bool

        Time:
            O(N)

        Raises:
            TypeError: 当key或other不是Set类型时抛出。
        """
        return get_members(self).isdisjoint(get_members(other))

    # subset

    def __le__(self, other):
        """ 测试集合是否是另一个集合的子集。

        Args:
            other: 一个python集合或集合key对象。

        Returns:
            bool

        Time:
            O(N)

        Raises:
            TypeError: 当key或other不是Set类型时抛出。
        """
        return get_members(self) <= get_members(other)

    # proper subset

    def __lt__(self, other):
        """ 测试集合是否是另一个集合的真子集。

        Args:
            other: 一个python集合或集合key对象。

        Returns:
            bool

        Time:
            O(N)

        Raises:
            TypeError: 当key或other不是Set类型时抛出。
        """
        return get_members(self) < get_members(other)

    # superset

    def __ge__(self, other):
        """ 测试集合是否是另一个集合的超集。

        Args:
            other: 一个python集合或集合key对象。

        Returns:
            bool

        Time:
            O(N)

        Raises:
            TypeError: 当key或other不是Set类型时抛出。
        """
        return get_members(self) >= get_members(other)

    # proper superset

    def __gt__(self, other):
        """ 测试集合是否是另一个集合的真超集。

        Args:
            other: 一个python集合或集合key对象。

        Returns:
            bool

        Time:
            O(N)

        Raises:
            TypeError: 当key或other不是Set类型时抛出。
        """
        return get_members(self) > get_members(other)

    # union

    def __or__(self, other):
        """ 返回集合和另一个集合的并集。

        Args:
            other: 一个python集合或集合key对象。

        Time:
            O(N)

        Returns:
            set

        Raises：
            TypeError: 当key或other不是Set类型时抛出。
        """
        return get_members(self) | get_members(other)

    __ror__ = __or__
    __ror__.__doc__ = """ __or__的反向方法，用于支持多集合对象进行并集操作。"""

    def __ior__(self, other):
        """ 求集合key对象和另一个集合key对象的并集， 并将结果保存到集合key对象self中。

        和 | 操作符不同，|= 操作符只能在集合key对象和集合key对象之间进行。

        Args:
            self: Python指定该方法必须返回self。

        Time:
            O(N)

        Returns:
            新的集合key对象的基数。

        Raises:
            TypeError: 当key或other不是Set类型时抛出。
        """
        try:
            if other.exists and other._represent != REDIS_TYPE['set']:
                raise TypeError

            self._client.sunionstore(self.name, [self.name, other.name])
            return self
        except redispy_exception.ResponseError:
            raise TypeError
 

    # intersection

    def __and__(self, other):
        """ 返回集合和另一个集合的交集。

        Args:
            other: 一个python集合或集合key对象。


        Time:
            O(N)

        Returns:
            set

        Raises：
            TypeError: 当key或other不是Set类型时抛出。
        """
        return get_members(self) & get_members(other)

    __rand__ = __and__
    __rand__.__doc__ = """ __and__的反向方法，用于支持多集合进行交集操作。 """

    def __iand__(self, other):
        """ 求集合key对象和另一个集合key对象的交集， 并将结果保存到集合key对象self中。

        和 & 操作符不同，&= 操作符只能在集合key对象和集合key对象之间进行。

        Args:
            self: Python指定该方法必须返回self。

        Time:
            O(N)

        Returns:
            新的集合key对象的基数。

        Raises:
            TypeError: 当key或other不是Set类型时抛出。
        """
        try:
            if other.exists and other._represent != REDIS_TYPE['set']:
                raise TypeError

            self._client.sinterstore(self.name, [self.name, other.name])
            return self
        except redispy_exception.ResponseError:
            raise TypeError

    # difference

    def __sub__(self, other):
        """ 返回集合对另一个集合的差集。

        Args:
            other: 一个python集合或集合key对象。

        Time:
            O(N)

        Returns:
            set

        Raises：
            TypeError: 当key或other不是Set类型时抛出。
        """
        return get_members(self) - get_members(other)

    def __rsub__(self, other):
        """ __sub__的反向方法，
        用于支持多集合进行差集运算。
        """
        # WARNING: 注意这里的位置不要弄反。
        return get_members(other) - get_members(self)

    def __isub__(self, other):
        """ 求集合key对象和另一个集合key对象的差集， 并将结果保存到集合key对象self中。

        和 - 操作符不同，-= 操作符只能在集合key对象和集合key对象之间进行。

        Args:
            self: Python指定该方法必须返回self。

        Time:
            O(N)

        Returns:
            新的集合key对象的基数。

        Raises:
            TypeError: 当key或other不是Set类型时抛出。
        """
        try:
            if other.exists and other._represent != REDIS_TYPE['set']:
                raise TypeError

            self._client.sdiffstore(self.name, [self.name, other.name])
            return self
        except redispy_exception.ResponseError:
            raise TypeError
 

    # symmetric difference

    def __xor__(self, other):
        """ 返回集合对另一个集合的对等差集。

        Args:
            other: 一个python集合或集合key对象。

        Returns:
            set

        Time:
            O(N)

        Raises:
            TypeError: 当key或other不是Set类型时抛出。
        """
        return get_members(self) ^ get_members(other)

    __rxor__ = __xor__
    __rxor__.__doc__ = \
    """ __xor__的反向方法，用于支持多集合的对等差集运算。 """
