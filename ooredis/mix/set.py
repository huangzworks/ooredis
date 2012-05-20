# coding:utf-8

__all__ = ['Set']

__metaclass__ = type

import collections
import redis.exceptions as redispy_exception

from ooredis.const import REDIS_TYPE
from ooredis.mix.key import Key
from ooredis.mix.helper import get_key_name_from_single_value, format_key

MOVE_FAIL_CAUSE_MEMBER_NOT_IN_SET = 0

class Set(Key):
    """ 集合 key 对象，底层实现是redis的set类型。 """

    def __repr__(self):
        return format_key(self, self.name, set(self))

    def __len__(self):
        """ 返回集合中元素的个数。
        当集合为空集时，返回 0 。

        Time:
            O(1)

        Returns:
            len 

        Raises:
            TypeError: 当 key 不是 redis 的 set 类型时抛出。
        """
        try:
            return self._client.scard(self.name)
        except redispy_exception.ResponseError:
            raise TypeError

    def __iter__(self):
        """ 返回一个包含集合中所有元素的迭代器。

        Time:
            O(N)

        Returns:
            iterator

        Raises:
            TypeError: 当 key 不是 redis 的 set 类型时抛出。
        """
        try:
            for redis_member in self._client.smembers(self.name):
                python_member = self._type_case.to_python(redis_member)
                yield python_member
        except redispy_exception.ResponseError:
            raise TypeError

    def __contains__(self, element):
        """ 检查给定元素 element 是否集合的成员。

        Args:
            element

        Time:
            O(1)

        Returns:
            bool: element是集合成员的话True，否则False。

        Raises:
            TypeError: 当 key 不是 redis 的 set 类型时抛出。
        """
        try:
            redis_element = self._type_case.to_redis(element)
            return self._client.sismember(self.name, redis_element)
        except redispy_exception.ResponseError:
            raise TypeError

    def add(self, element):
        """ 将 element 加入到集合当中。

        如果 element 已经是集合的成员，不做动作。
        如果 key 不存在，一个空集合被创建并执行 add 动作。

        Args:
            element

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 当 key 非空且它不是 redis 的 set 类型时抛出。
        """
        try:
            redis_element = self._type_case.to_redis(element)
            self._client.sadd(self.name, redis_element)
        except redispy_exception.ResponseError:
            raise TypeError

    def remove(self, element):
        """ 如果 element 是集合的成员，移除它。

        如果要移除的元素不存在，抛出 KeyError 。

        Args：
            element

        Time：
            O(1)

        Returns:
            None

        Raises:
            TypeError: 当 key 非空且它不是 redis 的 set 类型时抛出。
            KeyError： 要移除的元素 element 不存在于集合时抛出。
        """
        try:
            redis_element = self._type_case.to_redis(element)
            delete_success = self._client.srem(self.name, redis_element)
            if not delete_success:
                raise KeyError
        except redispy_exception.ResponseError:
            raise TypeError

    def pop(self):
        """ 移除并返回集合中任意一个成员。

        如果集合为空，抛出KeyError。

        Time：
            O(1)

        Returns:
            member: 被移除的集合成员。

        Raises:
            TypeError: 当 key 非空且它不是 redis 的 set 类型时抛出。
            KeyError: 集合为空集时抛出。
        """
        try:
            redis_member = self._client.spop(self.name)
            python_member = self._type_case.to_python(redis_member)
            if python_member is None:
                raise KeyError
            else:
                return python_member
        except redispy_exception.ResponseError:
            raise TypeError

    def random(self):
        """ 返回集合中的一个随机元素。

        该操作和 pop 相似，但 pop 将随机元素从集合中移除并返回，
        而 random 则仅仅返回随机元素，而不对集合进行任何改动。

        Time:
            O(1)

        Returns:
            member: 当集合非空时，返回一个成员。
            None: 当集合为空集时，返回 None 。

        Raises:
            TypeError: 当 key 非空且它不是 redis 的 set 类型时抛出。
        """
        try:
            redis_element = self._client.srandmember(self.name)
            python_member = self._type_case.to_python(redis_element)
            return python_member
        except redispy_exception.ResponseError:
            raise TypeError

    def move(self, destination, member):
        """ 将集合成员 member 移动到另一个集合 destination 中去。

        具体参考Redis命令：SMOVE。

        Args:
            destination: 指定被移动元素的目的地集合，
                         必须是一个集合 key 对象。
            member: 被移动的源集合的成员。

        Time:
            O(1)

        Returns:
            None

        Raises:
            KeyError: 要被移动的元素 member 不存在于集合时抛出。
            TypeError: 当 key 非空且它不是 redis 的 set 类型时抛出。
        """
        try:
            redis_member = self._type_case.to_redis(member)
            state = self._client.smove(self.name, destination.name, redis_member)
            if state == MOVE_FAIL_CAUSE_MEMBER_NOT_IN_SET:
                raise KeyError
        except redispy_exception.ResponseError:
            raise TypeError

    # disjoint, 不相交

    def isdisjoint(self, other):
        """ 检查集合是否和另一个集合不相交。

        Args:
            other: 一个 python 集合或集合 key 对象。
        
        Returns:
            bool

        Time:
            O(N)

        Raises:
            TypeError: 当 key 或 other 不是 Set 类型时抛出。
        """
        other_member = set(other)
        self_member = set(self)

        return self_member.isdisjoint(other_member)

    # subset, <= , 子集

    def __le__(self, other):
        """ 测试集合是否是另一个集合的子集。

        Args:
            other: 一个 python 集合或集合 key 对象。

        Returns:
            bool

        Time:
            O(N)

        Raises:
            TypeError: 当 key 或 other 不是 Set 类型时抛出。
        """
        return set(self) <= set(other)

    issubset = __le__

    # proper subset, < , 真子集

    def __lt__(self, other):
        """ 测试集合是否是另一个集合的真子集。

        Args:
            other: 一个 python 集合或集合 key 对象。

        Returns:
            bool

        Time:
            O(N)

        Raises:
            TypeError: 当 key 或 other 不是 Set 类型时抛出。
        """
        return set(self) < set(other)

    # superset, >= , 超集

    def __ge__(self, other):
        """ 测试集合是否是另一个集合的超集。

        Args:
            other: 一个 python 集合或集合 key 对象。

        Returns:
            bool

        Time:
            O(N)

        Raises:
            TypeError: 当 key 或 other 不是 Set 类型时抛出。
        """
        return set(self) >= set(other)

    issuperset = __ge__

    # proper superset, > , 真超集

    def __gt__(self, other):
        """ 测试集合是否是另一个集合的真超集。

        Args:
            other: 一个 python 集合或集合 key 对象。

        Returns:
            bool

        Time:
            O(N)

        Raises:
            TypeError: 当 key 或 other 不是 Set 类型时抛出。
        """
        return set(self) > set(other)

    # union, | , 并集

    def __or__(self, other):
        """ 返回集合和另一个集合的并集。

        Args:
            other: 一个 python 集合或集合 key 对象。

        Time:
            O(N)

        Returns:
            set

        Raises：
            TypeError: 当 key 或 other 不是 Set 类型时抛出。
        """
        return set(self) | set(other)

    __ror__ = __or__
    __ror__.__doc__ = """ __or__的反向方法，用于支持多集合对象进行并集操作。"""

    def __ior__(self, other):
        """
        计算 self 和 other 之间的并集，并将结果设置为 self 的值。
        other 可以是另一个集合 key 对象，或者 python set 的实例。

        Args:
            other

        Time:
            O(N)

        Returns:
            self: Python 指定该方法必须返回 self 。

        Raises:
            TypeError: 当 key 或 other 的类型不符合要求时抛出。
        """
        try:
            if isinstance(other, set):
                elements = set(self) | other
                redis_elements = map(self._type_case.to_redis, elements)
                self._client.sadd(self.name, *redis_elements)
            else:
                self._client.sunionstore(self.name, [self.name, other.name])

            return self
        except redispy_exception.ResponseError:
            raise TypeError
 
    # intersection, & , 交集

    def __and__(self, other):
        """ 返回集合和另一个集合的交集。

        Args:
            other: 一个 python 集合或集合 key 对象。

        Time:
            O(N)

        Returns:
            set

        Raises：
            TypeError: 当 key 或 other 不是 Set 类型时抛出。
        """
        return set(self) & set(other)

    __rand__ = __and__
    __rand__.__doc__ = """ __and__的反向方法，用于支持多集合进行交集操作。 """

    def __iand__(self, other):
        """
        计算 self 和 other 之间的交集，并将结果设置为 self 的值。
        other 可以是另一个集合 key 对象，或者 python set 的实例。

        Args:
            other

        Time:
            O(N)

        Returns:
            self: Python 指定该方法必须返回 self 。

        Raises:
            TypeError: 当 key 或 other 的类型不符合要求时抛出。
        """
        try:
            if isinstance(other, set):
                elements = set(self) - (set(self) & other)
                redis_elements = map(self._type_case.to_redis, elements)
                self._client.srem(self.name, *redis_elements)
            elif other.exists and other._represent != REDIS_TYPE['set']:
                raise TypeError
            else:
                self._client.sinterstore(self.name, [self.name, other.name])

            return self
        except redispy_exception.ResponseError:
            raise TypeError

    # difference, - , 差集

    def __sub__(self, other):
        """ 返回集合对另一个集合的差集。

        Args:
            other: 一个 python 集合或集合 key 对象。

        Time:
            O(N)

        Returns:
            set

        Raises：
            TypeError: 当 key 或 other 不是 Set 类型时抛出。
        """
        return set(self) - set(other)

    def __rsub__(self, other):
        """ __sub__的反向方法，
        用于支持多集合进行差集运算。
        """
        # WARNING: 注意这里的位置不要弄反。
        return set(other) - set(self)

    def __isub__(self, other):
        """
        计算 self 和 other 之间的差集，并将结果设置为 self 的值。
        other 可以是另一个集合 key 对象，或者 python set 的实例。

        Args:
            other

        Time:
            O(N)

        Returns:
            self: Python指定该方法必须返回self。

        Raises:
            TypeError: 当 key 或 other 的类型不符合要求时抛出。
        """
        try:
            if isinstance(other, set):
                remove_elements = set(self) & other
                redis_elements = map(self._type_case.to_redis, remove_elements)
                self._client.srem(self.name, *redis_elements)
            else:
                self._client.sdiffstore(self.name, [self.name, other.name])

            return self
        except redispy_exception.ResponseError:
            raise TypeError

    # symmetric difference, ^ ， 对等差

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
        return set(self) ^ set(other)

    __rxor__ = __xor__
    __rxor__.__doc__ = \
    """ __xor__的反向方法，用于支持多集合的对等差集运算。 """
