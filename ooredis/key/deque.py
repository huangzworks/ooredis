# coding: utf-8

__all__ = ['Deque']

__metaclass__ = type

import redis.exceptions as redispy_exception

from ooredis.key.base_key import BaseKey
from ooredis.key.helper import format_key, wrap_exception

from common_key_property_mixin import CommonKeyPropertyMixin

class Deque(BaseKey, CommonKeyPropertyMixin):

    """ 
    一个双端队列 key 对象，底层实现是 redis 的 list 类型。 
    """

    def append(self, python_item):
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
        redis_item = self.encode(python_item)
        self._client.rpush(self.name, redis_item)


    @wrap_exception
    def appendleft(self, python_item):
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
        redis_item = self.encode(python_item)
        self._client.lpush(self.name, redis_item)


    def extend(self, python_iterable):
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
        redis_iterable = map(self.encode, python_iterable)
        self._client.rpush(self.name, *redis_iterable)


    @wrap_exception
    def extendleft(self, python_iterable):
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
        redis_iterable = map(self.encode, python_iterable)
        self._client.lpush(self.name, *redis_iterable)


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
    

    def count(self, python_item):
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
        all_python_item = list(self)
        return all_python_item.count(python_item)


    @wrap_exception
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
        redis_item = self._client.rpop(self.name)
        python_item = self.decode(redis_item)
        if python_item is None:
            raise IndexError
        else:
            return python_item


    @wrap_exception
    def block_pop(self, timeout=0):
        """
        移除并返回队列最右边的元素，
        如果队列中没有元素，那么阻塞 timeout 秒，直到获取元素或超时为止。

        Args:
            timeout: 等待元素时的最大阻塞秒数

        Time:
            O(1)

        Returns:
            None: 超时时返回
            pop_item: 被弹出的元素

        Raises:
            TypeError: 尝试对非 list 类型的 key 进行操作时抛出。
        """
        # 每个非空 brpop 的结果都是一个列表 ['list of the pop item', 'pop item']
        redis_queue_name_and_item_list = self._client.brpop(self.name, timeout)
        if redis_queue_name_and_item_list is not None:
            redis_item = redis_queue_name_and_item_list[1]
            python_item = self.decode(redis_item)
            return python_item


    @wrap_exception
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
        redis_item = self._client.lpop(self.name)
        python_item = self.decode(redis_item)
        if python_item is None:
            raise IndexError
        else:
            return python_item


    @wrap_exception
    def block_popleft(self, timeout=0):
        """
        移除并返回队列最左边的元素，
        如果队列中没有元素，那么阻塞 timeout 秒，直到获取元素或超时为止。

        Args:
            timeout: 等待元素时的最大阻塞秒数

        Time:
            O(1)

        Returns:
            None: 超时时返回
            pop_item: 被弹出的元素

        Raises:
            TypeError: 尝试对非 list 类型的 key 进行操作时抛出。
        """
        # 每个非空 blpop 的结果都是一个列表 ['list of the pop item', 'pop item']
        redis_queue_name_and_item_list = self._client.blpop(self.name, timeout)
        if redis_queue_name_and_item_list is not None:
            redis_item = redis_queue_name_and_item_list[1]
            python_item = self.decode(redis_item) 
            return python_item


    def __repr__(self):
        return format_key(self, self.name, list(self))


    @wrap_exception
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
        return self._client.llen(self.name)


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
            all_redis_item = self._client.lrange(self.name, 0, -1)
            for redis_item in all_redis_item:
                python_item = self.decode(redis_item)
                yield python_item
        except redispy_exception.ResponseError:
            raise TypeError

    
    def __delitem__(self, index):
        """
        删除列表中给定 index 上的值。

        Args:
            index ：可以是单个 key ，也可以是一个表示范围的 slice 。
            item

        Time:
            O(N)

        Returns:
            None

        Raises:
            TypeError: 尝试对非 list 类型的 key 进行操作时抛出。
        """
        # TODO: 这个实现带有竞争条件
        all_python_item = list(self)
        del all_python_item[index]
        self.delete()
        if all_python_item != []:
            self.extend(all_python_item)
        """
        # del self[index]
        # ...

        # del self[:]
        if key.start is None and key.stop is None:
            self.delete()

        # del self[i:]
        if key.start is not None and key.stop is None:
            self._client.ltrim(self.name, 0, key.start-1)

        # del self[:j]
        if key.start is None and key.stop is not None:
            self._client.ltrim(self.name, key.stop, -1)

        # del self[i:j]
        # ...
        """


    def __getitem__(self, index):
        """
        返回列表中给定 index 上的值。

        Args:
            index ：可以是单个 key ，也可以是一个表示范围的 slice 。
            item

        Time:
            O(N)

        Returns:
            None

        Raises:
            TypeError: 尝试对非 list 类型的 key 进行操作时抛出。
        """
        return list(self)[index]


    def __setitem__(self, index, item):
        """
        将列表中给定 index 上的值设置为 item 。

        Args:
            index ：可以是单个 key ，也可以是一个表示范围的 slice 。
            item

        Time:
            O(N)

        Returns:
            None

        Raises:
            TypeError: 尝试对非 list 类型的 key 进行操作时抛出。
        """
        # TODO: 这个实现带有竞争条件
        all_python_item = list(self)
        all_python_item[index] = item
        self.delete()
        if all_python_item != []:
            self.extend(all_python_item)
