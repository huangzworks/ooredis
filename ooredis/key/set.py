# coding:utf-8

__all__ = ['Set']

__metaclass__ = type

import redis
import collections

from ooredis.const import REDIS_TYPE

from base_key import BaseKey
from helper import format_key, wrap_exception
from common_key_property_mixin import CommonKeyPropertyMixin

REMOVE_SUCCESS = True
MOVE_FAIL_CAUSE_MEMBER_NOT_IN_SET = 0

class Set(BaseKey, CommonKeyPropertyMixin):

    """
    将 Redis 的 Set 结构映射为集合对象。
    """

    def __repr__(self):
        return format_key(self, self.name, set(self))


    @wrap_exception
    def add(self, element):
        """ 
        将 element 加入到集合当中。

        如果 element 已经是集合的成员，不做动作。
        如果 key 不存在，一个空集合被创建并执行 add 动作。

        Args:
            element

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 当 key 非空且它不是 Redis 的 set 类型时抛出。
        """
        redis_element = self._encode(element)
        self._client.sadd(self.name, redis_element)


    @wrap_exception
    def remove(self, element):
        """ 
        如果 element 是集合的成员，移除它。

        如果要移除的元素不存在，抛出 KeyError 。

        Args：
            element

        Time：
            O(1)

        Returns:
            None

        Raises:
            TypeError: 当 key 非空且它不是 Redis 的 set 类型时抛出。
            KeyError： 要移除的元素 element 不存在于集合时抛出。
        """
        redis_element = self._encode(element)
        remove_state = self._client.srem(self.name, redis_element)
        if remove_state != REMOVE_SUCCESS:
            raise KeyError


    @wrap_exception
    def pop(self):
        """ 
        移除并返回集合中任意一个成员。
        如果集合为空，抛出 KeyError 。

        Args:
            None

        Time：
            O(1)

        Returns:
            member: 被移除的集合成员。

        Raises:
            TypeError: 当 key 非空且它不是 Redis 的 set 类型时抛出。
            KeyError: 集合为空集时抛出。
        """
        redis_member = self._client.spop(self.name)
        if redis_member is None:
            raise KeyError

        python_member = self._decode(redis_member)
        return python_member


    @wrap_exception
    def random(self):
        """ 
        随机返回集合中的某个元素。

        该操作和 pop 方法相似，但 pop 将随机元素从集合中移除并返回，
        而 random 则仅仅返回随机元素，而不对集合进行任何改动。

        Args:
            None

        Time:
            O(1)

        Returns:
            member: 当集合非空时，返回一个成员。
            None: 当集合为空集时，返回 None 。

        Raises:
            TypeError: 当 key 非空且它不是 Redis 的 set 类型时抛出。
        """
        redis_element = self._client.srandmember(self.name)
        python_member = self._decode(redis_element)
        return python_member


    @wrap_exception
    def move(self, destination, member):
        """ 
        将集合成员 member 移动到另一个集合 destination 中去。

        具体参考 Redis 命令：SMOVE。

        Args:
            destination: 指定被移动元素的目的地集合， 必须是一个集合 key 对象。
            member: 被移动的源集合的成员。

        Time:
            O(1)

        Returns:
            None

        Raises:
            KeyError: 要被移动的元素 member 不存在于集合时抛出。
            TypeError: 当 key 非空且它不是 Redis 的 set 类型时抛出。
        """
        redis_member = self._encode(member)
        state = self._client.smove(self.name, destination.name, redis_member)
        if state == MOVE_FAIL_CAUSE_MEMBER_NOT_IN_SET:
            raise KeyError


    # disjoint, 不相交

    def isdisjoint(self, other):
        """ 
        检查集合是否和另一个集合不相交。

        Args:
            other: 一个 Python 集合或集合 Key 对象。
        
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
        """ 
        测试集合是否是另一个集合的子集。

        Args:
            other: 一个 Python 集合或集合 key 对象。

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
        """ 
        测试集合是否是另一个集合的真子集。

        Args:
            other: 一个 Python 集合或集合 key 对象。

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
        """ 
        测试集合是否是另一个集合的超集。

        Args:
            other: 一个 Python 集合或集合 key 对象。

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
        """ 
        测试集合是否是另一个集合的真超集。

        Args:
            other: 一个 Python 集合或集合 key 对象。

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
        """ 
        返回集合和另一个集合的并集。

        Args:
            other: 一个 Python 集合或集合 key 对象。

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


    @wrap_exception
    def __ior__(self, other):
        """
        计算 self 和 other 之间的并集，并将结果设置为 self 的值。
        other 可以是另一个集合 key 对象，或者 Python set 的实例。

        Args:
            other

        Time:
            O(N)

        Returns:
            self: Python 指定该方法必须返回 self 。

        Raises:
            TypeError: 当 key 或 other 的类型不符合要求时抛出。
        """
        if isinstance(other, set):
            python_elements = set(self) | other
            redis_elements = map(self._encode, python_elements)
            self._client.sadd(self.name, *redis_elements)
        else:
            self._client.sunionstore(self.name, [self.name, other.name])

        return self
 

    # intersection, & , 交集

    def __and__(self, other):
        """ 
        返回集合和另一个集合的交集。

        Args:
            other: 一个 Python 集合或集合 key 对象。

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


    @wrap_exception
    def __iand__(self, other):
        """
        计算 self 和 other 之间的交集，并将结果设置为 self 的值。
        other 可以是另一个集合 key 对象，或者 Python set 的实例。

        Args:
            other

        Time:
            O(N)

        Returns:
            self: Python 指定该方法必须返回 self 。

        Raises:
            TypeError: 当 key 或 other 的类型不符合要求时抛出。
        """
        if isinstance(other, set):
            python_elements = set(self) - (set(self) & other)
            redis_elements = map(self._encode, python_elements)
            self._client.srem(self.name, *redis_elements)
        elif other.exists and other._represent != REDIS_TYPE['set']:
            raise TypeError
        else:
            self._client.sinterstore(self.name, [self.name, other.name])

        return self


    # difference, - , 差集

    def __sub__(self, other):
        """ 
        返回集合对另一个集合的差集。

        Args:
            other: 一个 Python 集合或集合 key 对象。

        Time:
            O(N)

        Returns:
            set

        Raises：
            TypeError: 当 key 或 other 不是 Set 类型时抛出。
        """
        return set(self) - set(other)


    def __rsub__(self, other):
        """ 
        __sub__的反向方法，
        用于支持多集合进行差集运算。
        """
        # WARNING: 注意这里的位置不要弄反。
        return set(other) - set(self)


    @wrap_exception
    def __isub__(self, other):
        """
        计算 self 和 other 之间的差集，并将结果设置为 self 的值。
        other 可以是另一个集合 key 对象，或者 Python set 的实例。

        Args:
            other

        Time:
            O(N)

        Returns:
            self: Python指定该方法必须返回self。

        Raises:
            TypeError: 当 key 或 other 的类型不符合要求时抛出。
        """
        if isinstance(other, set):
            python_elements = set(self) & other
            redis_elements = map(self._encode, python_elements)
            self._client.srem(self.name, *redis_elements)
        else:
            self._client.sdiffstore(self.name, [self.name, other.name])

        return self


    # symmetric difference, ^ ， 对等差

    def __xor__(self, other):
        """ 
        返回集合对另一个集合的对等差集。

        Args:
            other: 一个Python集合或集合key对象。

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


    @wrap_exception
    def __len__(self):
        """ 
        返回集合中元素的个数。
        当集合为空集时，返回 0 。

        Args:
            None

        Time:
            O(1)

        Returns:
            len 

        Raises:
            TypeError: 当 key 不是 Redis 的 set 类型时抛出。
        """
        return self._client.scard(self.name)


    def __iter__(self):
        """ 
        返回一个包含集合中所有元素的迭代器。

        Time:
            O(N)

        Returns:
            iterator

        Raises:
            TypeError: 当 key 不是 Redis 的 set 类型时抛出。
        """
        try:
            for redis_member in self._client.smembers(self.name):
                python_member = self._decode(redis_member)
                yield python_member
        except redis.exceptions.ResponseError:
            raise TypeError


    @wrap_exception
    def __contains__(self, element):
        """ 
        检查给定元素 element 是否集合的成员。

        Args:
            element

        Time:
            O(1)

        Returns:
            bool: element 是集合成员的话返回 True ，否则返回 False 。

        Raises:
            TypeError: 当 key 不是 Redis 的 set 类型时抛出。
        """
        redis_element = self._encode(element)
        return self._client.sismember(self.name, redis_element)
