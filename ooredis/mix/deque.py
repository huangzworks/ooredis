# coding: utf-8

__all__ = ['Deque']

__metaclass__ = type

import collections
import redis.exceptions as redispy_exception

from ooredis.mix.key import Key
from ooredis.mix.helper import format_key

class Deque(Key):
    """ 一个双端队列 key 对象，底层实现是 redis 的 list 类型。 """

    def append(self, item):
        """
        将元素 item 追加到队列的最右边。

        Args:
            item

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 尝试对非 list 类型的 key 进行操作时抛出。
        """
        try:
            self._client.rpush(self.name, item)
        except redispy_exception.ResponseError:
            raise TypeError

    def appendleft(self, item):
        """
        将元素 item 追加到队列的最左边。

        Args:
            item

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 尝试对非 list 类型的 key 进行操作时抛出。
        """
        try:
            self._client.lpush(self.name, item)
        except redispy_exception.ResponseError:
            raise TypeError

    def extend(self, iterable):
        """
        将 iterable 内的所有元素追加到队列的最右边。

        Args:
            iterable

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 尝试对非 list 类型的 key 进行操作时抛出。
        """
        try:
            self._client.rpush(self.name, *iterable)
        except redispy_exception.ResponseError:
            raise TypeError

    def extendleft(self, iterable):
        """
        将 iterable 内的所有元素追加到队列的最左边。

        注意被追加元素是以逆序排列的。

        比如对一个空队列 d 执行 d.extendleft(range(3)) ，
        那么队列 d 将变成 [3, 2, 1] 。

        Args:
            iterable

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 尝试对非 list 类型的 key 进行操作时抛出。
        """
        try:
            self._client.lpush(self.name, *iterable)
        except redispy_exception.ResponseError:
            raise TypeError

    def clear(self):
        """
        删除队列中的所有元素。

        Time:
            O(1)
        
        Returns:
            None

        Raises:
            None
        """
        self.delete()
    
    def count(self, item):
        """
        计算队列中和 item 相等的元素的个数。

        Args:
            item

        Time:
            O(N)

        Returns:
            count

        Raises:
            TypeError: 尝试对非 list 类型的 key 进行操作时抛出。
        """
        all_item = list(self)
        return all_item.count(item)

    def pop(self):
        """
        移除并返回队列最右边的元素。

        如果队列为空， 抛出 IndexError 。

        Args:
            None

        Time:
            O(1)

        Returns:
            pop_item

        Raises:
            IndexError: 尝试对空队列执行 pop 操作时抛出。
            TypeError: 尝试对非 list 类型的 key 进行操作时抛出。
        """
        try:
            item = self._client.rpop(self.name)
            if item is None:
                raise IndexError
            else:
                return item
        except redispy_exception.ResponseError:
            raise TypeError

    def popleft(self):
        """
        移除并返回队列最左边的元素。

        如果队列为空，抛出 IndexError 。

        Args:
            None

        Time:
            O(1)

        Returns:
            pop_item

        Raises:
            IndexError: 尝试对空队列执行 pop 操作时抛出。
            TypeError: 尝试对非 list 类型的 key 进行操作时抛出。
        """
        try:
            item = self._client.lpop(self.name)
            if item is None:
                raise IndexError
            else:
                return item
        except redispy_exception.ResponseError:
            raise TypeError

    def __repr__(self):
        return format_key(self, self.name, list(self))

    def __len__(self):
        """
        返回队列中的元素个数。
        空列表返回 0 。

        Time:
            O(1)

        Returns:
            len

        Raises:
            TypeError: 尝试对非 list 类型的 key 进行操作时抛出。
        """
        try:
            return self._client.llen(self.name)
        except redispy_exception.ResponseError:
            raise TypeError

    def __iter__(self):
        """
        返回一个包含整个队列所有元素的迭代器。

        Time:
            O(N)

        Returns:
            iterator

        Raises:
            TypeError: 尝试对非 list 类型的 key 进行操作时抛出。
        """
        try:
            all_item = self._client.lrange(self.name, 0, -1)
            for item in all_item:
                yield item
        except redispy_exception.ResponseError:
            raise TypeError

    def __delitem__(self, key):
        raise Exception 

    def __getitem__(self, index):
        all_item = list(self)
        return all_item[index]

    def __setitem__(self, index, item):
        raise Exception
