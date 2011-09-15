# coding: utf-8

__all__ = ['SortedSet']

__metaclass__ = type

import redis.exceptions as redispy_exception
from functools import partial

from ooredis.mix.key import Key
from ooredis.const import (
    LEFTMOST,
    RIGHTMOST,
    DEFAULT_INCREMENT,
    DEFAULT_DECREMENT,
)

# redis command execute status code
MEMBER_NOT_IN_SET_AND_REMOVE_FALSE = 0
MEMBER_NOT_IN_SET_AND_DELETE_FALSE = 0
MEMBER_NOT_IN_SET_AND_GET_RANK_FALSE = None
MEMBER_NOT_IN_SET_AND_GET_SCORE_FALSE = None

# ZRANGE result item index
VALUE = 0
SCORE= 1

class SortedSet(Key):
    """ 有序集对象，底层是redis的zset实现。 """

    def __repr__(self):
        key_type = self.__class__.__name__.title()
        key_name = self.name
        key_values = list(self)
        return "{0} Key '{1}': {2}".format(key_type, key_name, key_values)
    
    def __len__(self):
        """ 返回有序集的基数。
        
        Time:
            O(1)

        Returns:
            int: 有序集的基数，集合不存在或为空时返回0。

        Raises：
            TypeError: 当key不是有序集类型时抛出。
        """
        try:
            return self._client.zcard(self.name)
        except redispy_exception.ResponseError:
            raise TypeError

    def __contains__(self, element):
        """ 检查给定元素是否是有序集的成员。 

        Args:
            element: 要检查的元素。

        Time:
            O(1)

        Returns:
            bool: 如果element是集合的成员，返回True，否则False。

        Raises:
            TypeError: 当key不是有序集类型时抛出。
        """
        # NOTE:
        # 因为在redis里有序集zset没有集合set那样的SISMEMBER命令，
        # 所以这里用ZSCORE命令hack一个，
        # 如果ZSCORE key member不为None，证明element是有序集成员。

        # WARNING: 这里不要用self.score，这两个方法互相引用。
        try:
            element = self._type_case.to_redis(element)
            return None != self._client.zscore(self.name, element)
        except redispy_exception.ResponseError:
            raise TypeError

    def __setitem__(self, member, score):
        """ 将元素的member的score值设为score。

        如果member不存在于有序集，将member加入到有序集。

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 当key不是有序集类型时抛出。
        """
        try:
            member = self._type_case.to_redis(member)
            self._client.zadd(self.name, member, score) 
        except redispy_exception.ResponseError:
            raise TypeError

    def __getitem__(self, index):
        """ 返回有序集指定下标内的元素。

        Args:
            index: 一个下标或一个slice对象。

        Returns:
            dict： 使用下标时，返回一个字典，包含value和score。
            list：使用slice对象时，返回一个列表，
                  列表中每个项都是一个字典。

        Time:
            O(log(N)+M)，N为有序集的基数，而M为结果集的基数。

        Raises:
            KeyError: index下标超出范围时抛出。
            TypeError: 当key不是有序集类型时抛出。
        """
        try:
            item_to_dict_list = partial(map, lambda item: dict(value=self._type_case.to_python(item[VALUE]), score=item[SCORE]))

            if isinstance(index, slice):
                items = self._client.zrange(self.name, LEFTMOST, RIGHTMOST, withscores=True)
                return item_to_dict_list(items[index])
            else:
                items = self._client.zrange(self.name, index, index, withscores=True)
                return item_to_dict_list(items)[0]
        except redispy_exception.ResponseError:
            raise TypeError

    def __delitem__(self, index):
        """ 删除有序集指定下标内的元素。

        Args:
            index: 下标或一个slice对象。

        Time:
            O(log(N)+M)，N为有序集的基数，而M为被移除成员的数量。

        Returns:
            None

        Raises:
            KeyError: index下标超出范围时抛出。
            TypeError: 当key不是有序集类型时抛出。
        """
        try:
            if isinstance(index, slice):
                start = LEFTMOST if index.start == None else index.start
                stop = RIGHTMOST if index.stop == None else index.stop-1

                self._client.zremrangebyrank(self.name, start, stop)
            else:
                if self._client.zremrangebyrank(self.name, index, index) == \
                   MEMBER_NOT_IN_SET_AND_DELETE_FALSE:
                    raise IndexError
        except redispy_exception.ResponseError:
            raise TypeError

    def remove(self, member, check=False):
        """ 移除有序集成员member，如果member不存在，不做动作。

        Args:
            member: 要移除的成员。
            check: 是否检查member必须在有序集合中。

        Time:
            O(log(N))

        Returns:
            None

        Raises:
            TypeError: 当key不是有序集类型时抛出。
            KeyError: 当member不存在且check为True时抛出。
        """
        try:
            member = self._type_case.to_redis(member)
            status = self._client.zrem(self.name, member)
            if check and status == MEMBER_NOT_IN_SET_AND_REMOVE_FALSE:
                raise KeyError
        except redispy_exception.ResponseError:
            raise TypeError

    def rank(self, member, reverse=False):
        """ 返回有序集中成员member的score值的排名。

        排序可以选择递增(从小到大)和递减(从大到小)两种顺序，
        默认为递增序排序。

        Args:
            member: 被检查的成员。
            reverse: 如果为True，元素以递减排序。

        Time:
            O(log(N))

        Returns:
            int: member的score排名。

        Raises:
            KeyError: 当member不在有序集中时抛出。
            TypeError: 当key不是有序集类型时由in语句抛出。
        """
        try:
            member = self._type_case.to_redis(member)

            get_rank = self._client.zrevrank if reverse else self._client.zrank
            result = get_rank(self.name, member)

            if result == MEMBER_NOT_IN_SET_AND_GET_RANK_FALSE:
                raise KeyError
            else:
                return result
        except redispy_exception.ResponseError:
            raise TypeError

    def score(self, member):
        """ 返回有序集中成员member的score值。

        Args:
            member

        Time:
            O(1)

        Returns:
            float: 以浮点值表示的score值。

        Raises:
            KeyError: 当member不在有序集中时抛出。
            TypeError: 当key不是有序集类型时抛出，由in语句抛出。
        """
        try:
            member = self._type_case.to_redis(member)
            result = self._client.zscore(self.name, member)

            if result == MEMBER_NOT_IN_SET_AND_GET_SCORE_FALSE:
                raise KeyError
            else:
                return result
        except redispy_exception.ResponseError:
            raise TypeError

    def incr(self, member, increment=DEFAULT_INCREMENT):  
        """ 将member的score值加上increment。 

        当key不存在，或member不是key的成员时，
        self.incr(member, increment)等同于self[member] = increment

        Args:
            member: 集合成员
            increment：增量，默认为1。

        Time:
            O(log(N))

        Returns:
            float: member成员的新score值。

        Raises:
            TypeError: 当key不是有序集类型时抛出。
        """
        try:
            member = self._type_case.to_redis(member)
            return self._client.zincrby(self.name, member, increment)
        except redispy_exception.ResponseError:
            raise TypeError

    def decr(self, member, decrement=DEFAULT_DECREMENT):
        """ 将member的score值减去decrement。 

        当key不存在，或member不是key的成员时，
        self.decr(member, decrement)等同于self[member] = 0-decrement

        Args:
            member: 集合成员
            decrement：减量，默认为1。

        Time:
            O(log(N))

        Returns:
            float: member成员的新score值。

        Raises:
            TypeError: 当key不是有序集类型时抛出。
        """
        return self.incr(member, 0-decrement)
