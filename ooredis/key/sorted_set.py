# coding: utf-8

__all__ = ['SortedSet']

__metaclass__ = type

from functools import partial
from ooredis.const import (
    LEFTMOST,
    RIGHTMOST,
    DEFAULT_INCREMENT,
    DEFAULT_DECREMENT,
)

from base_key import BaseKey
from helper import format_key, wrap_exception
from common_key_property_mixin import CommonKeyPropertyMixin

# redis command execute status code
MEMBER_NOT_IN_SET_AND_REMOVE_FALSE = 0
MEMBER_NOT_IN_SET_AND_DELETE_FALSE = 0
MEMBER_NOT_IN_SET_AND_GET_SCORE_FALSE = None

# ZRANGE result item index
VALUE = 0
SCORE= 1

class SortedSet(BaseKey, CommonKeyPropertyMixin):

    """ 
    将 Redis 的 sorted set 结构映射为有序集对象。
    """

    def __repr__(self):
        return format_key(self, self.name, list(self))
  

    @wrap_exception
    def __len__(self):
        """ 
        返回有序集的基数。

        Args:
            None

        Time:
            O(1)

        Returns:
            int: 有序集的基数，集合不存在或为空时返回0。

        Raises：
            TypeError: 当key不是有序集类型时抛出。
        """
        return self._client.zcard(self.name)


    @wrap_exception
    def __contains__(self, element):
        """ 
        检查给定元素 element 是否是有序集的成员。 

        Args:
            element

        Time:
            O(log(N))

        Returns:
            bool: 如果 element 是集合的成员，返回 True ，否则 False 。

        Raises:
            TypeError: 当 key 不是有序集类型时抛出。
        """
        # 因为在 redis 里 zset 没有 set 那样的 SISMEMBER 命令，
        # 所以这里用 ZSCORE 命令 hack 一个：
        # 如果 ZSCORE key member 不为 None ，证明 element 是有序集成员。
        # 注意，这里不能用 self.score 来实现，因为这两个方法互相引用。
        redis_element = self._encode(element)
        element_score = self._client.zscore(self.name, redis_element)
        return element_score is not None


    @wrap_exception
    def __setitem__(self, member, new_score):
        """ 
        将元素 member 的 score 值更新为 new_score 。

        如果 member 不存在于有序集，
        那么将 member 加入到有序集， score 值等于 new_score 。

        Args:
            member
            new_score

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 当key不是有序集类型时抛出。
        """
        redis_memeber = self._encode(member)
        self._client.zadd(self.name, redis_memeber, new_score)


    @wrap_exception
    def __getitem__(self, index):
        """ 
        返回有序集指定下标内的元素。

        Args:
            index: 一个下标或一个 slice 对象。

        Returns:
            dict： 使用下标时，返回一个字典，包含 value 和 score 。
            list：使用 slice 对象时，返回一个列表，
                  列表中每个项都是一个字典。

        Time:
            O(log(N)+M) ， N 为有序集的基数，而 M 为结果集的基数。

        Raises:
            KeyError: index 下标超出范围时抛出。
            TypeError: 当 key 不是有序集类型时抛出。
        """
        item_to_dict_list = \
            partial(map,
                    lambda item: dict(
                        value=self._decode(item[VALUE]), 
                        score=item[SCORE]
                    ))

        if isinstance(index, slice):
            items = self._client.zrange(self.name, LEFTMOST, RIGHTMOST, withscores=True)
            return item_to_dict_list(items[index])
        else:
            items = self._client.zrange(self.name, index, index, withscores=True)
            return item_to_dict_list(items)[0]


    @wrap_exception
    def __delitem__(self, index):
        """ 
        删除有序集指定下标内的元素。

        Args:
            index: 下标或一个 slice 对象。

        Time:
            O(log(N)+M) ， N 为有序集的基数，而 M 为被移除成员的数量。

        Returns:
            None

        Raises:
            KeyError: index 下标超出范围时抛出。
            TypeError: 当 key 不是有序集类型时抛出。
        """
        if isinstance(index, slice):
            start = LEFTMOST if index.start is None else index.start
            stop = RIGHTMOST if index.stop is None else index.stop-1

            self._client.zremrangebyrank(self.name, start, stop)
        else:
            status = self._client.zremrangebyrank(self.name, index, index)
            if status == MEMBER_NOT_IN_SET_AND_DELETE_FALSE:
                raise IndexError


    @wrap_exception
    def remove(self, member):
        """ 
        移除有序集成员 member ，如果 member 不存在，不做动作。

        Args:
            member: 要移除的成员。

        Time:
            O(log(N))

        Returns:
            None

        Raises:
            TypeError: 当 key 不是有序集类型时抛出。
        """
        redis_member = self._encode(member)
        self._client.zrem(self.name, redis_member)


    @wrap_exception
    def rank(self, member):
        """ 
        按从小到大的顺序(正序)返回有序集成员 member 的 score 值的排名。

        Args:
            member: 被检查的成员。

        Time:
            O(log(N))

        Returns:
            None: 当 member 不是有序集的成员时返回
            int: member 的 score 排名。

        Raises:
            TypeError: 当 key 不是有序集类型时由 in 语句抛出。
        """
        redis_member = self._encode(member)
        return self._client.zrank(self.name, redis_member)


    @wrap_exception
    def reverse_rank(self, member):
        """
        按从大到小的顺序(逆序)返回有序集成员 member 的 score 值排名。

        Args:
            member

        Time:
            O(log(N))

        Returns:
            None: 当 member 不是有序集的成员时返回
            int: member 的 score 值排名

        Raises:
            TypeError: 当 key 不是有序集类型时由 in 语句抛出。
        """
        redis_member = self._encode(member)
        return self._client.zrevrank(self.name, redis_member)


    @wrap_exception
    def score(self, member):
        """ 
        返回有序集中成员 member 的 score 值。

        Args:
            member

        Time:
            O(1)

        Returns:
            None: 当 member 不是有序集的成员时返回
            float: 以浮点值表示的 score 值。

        Raises:
            TypeError: 当 key 不是有序集类型时抛出，由 in 语句抛出。
        """
        redis_member = self._encode(member)
        return self._client.zscore(self.name, redis_member)


    @wrap_exception
    def incr(self, member, increment=DEFAULT_INCREMENT):  
        """ 
        将 member 的 score 值加上 increment 。 

        当 key 不存在，或 member 不是 key 的成员时，
        self.incr(member, increment) 等同于 self[member] = increment

        Args:
            member: 集合成员
            increment: 增量，默认为1。

        Time:
            O(log(N))

        Returns:
            float: member 成员的新 score 值。

        Raises:
            TypeError: 当 key 不是有序集类型时抛出。
        """
        redis_member = self._encode(member)
        return self._client.zincrby(self.name, redis_member, increment)


    def decr(self, member, decrement=DEFAULT_DECREMENT):
        """ 
        将 member 的 score 值减去 decrement 。 

        当 key 不存在，或 member 不是 key 的成员时，
        self.decr(member, decrement) 等同于 self[member] = 0-decrement

        Args:
            member: 集合成员
            decrement: 减量，默认为 1 。

        Time:
            O(log(N))

        Returns:
            float: member 成员的新 score 值。

        Raises:
            TypeError: 当 key 不是有序集类型时抛出。
        """
        return self.incr(member, 0-decrement)
