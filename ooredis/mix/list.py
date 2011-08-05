# coding:utf-8

__all__ = ['List']

__metaclass__ = type

import collections
import redis.exceptions as redispy_exception

from ooredis.mix.key import (
    get_key_name_from_single_value,
    Key,
)
from ooredis.const import LEFTMOST, RIGHTMOST

# block time
INDEFINITELY = 0

# remove mode
REMOVE_ALL_ELEMENT_EQUAL_VALUE = 0

# redis blpop/brpop result index
VALUE = 1

# NOTE:
# redis的list是可变的(mutable)，没有继承MutableSequence主要是
# 考虑到python的列表是单向增长的(从左到右)，
# 而redis的列表是双向的，append、pop等和redis的表现不同。
class List(Key, collections.Sequence):
    """ 一个列表key对象，底层实现是redis的list类型。 """

    def __repr__(self):
        key_type = self.__class__.__name__.title()
        key_name = self.name
        key_values = list(self)
        return "{0} Key '{1}': {2}".format(key_type, key_name, key_values)

    def __len__(self):
        """ 返回列表中的元素个数。
        不存在的列表返回0。

        Time:
            O(1)

        Returns:
            int: 元素个数。

        Raises：
            TypeError: 尝试对非list类型的对象进行操作时抛出。
        """
        try:
            return self._client.llen(self.name)
        except redispy_exception.ResponseError:
            raise TypeError

    def __setitem__(self, key, value):
        """ 将列表指定位置的值设为value。

        暂时只支持对单个key赋值，像这样list[2] = 'hi'，
        不支持list[2:4] = ['go']这样的range赋值。

        Args:
            key: 指定列表的位置。
            value: 要设置的值。

        Time:
            O(1)

        Returns:
            None

        Raises:
            IndexError: key超出范围。
            TypeError: 当key对象不存在，
                       或对非list类型的对象进行操作时抛出。
            NotImplementedError: 当使用range赋值时抛出。
        """
        # TODO: 支持range赋值？

        # NOTE:
        # redis-py对不存的key，以及key超出范围都抛出ResponseError
        # ooredis里__getitem__和__setitem__对不存在的key都抛出IndexError
        # 主要是为了和python的list类型行为保持一致。
        if self.exists == False:
            raise IndexError

        if isinstance(key, slice):
            # 没有实现列表的range赋值，
            # 因为redis没有相应的函数。
            raise NotImplementedError
        elif key >= len(self):
            raise IndexError
        else:
            try:
                value = self._type_case.to_redis(value)
                self._client.lset(self.name, key, value)
            except redispy_exception.ResponseError:
                raise TypeError

    def __getitem__(self, key):
        """ 获取特定位置key上的列表元素。

        Args:
            key: 一个索引，或一个range。

        Time:
            获取表头或表尾为O(1)，其他为O(N)

        Returns:
            value: 列表元素。

        Raises:
            IndexError: 当key对象不存在，或key超出范围时抛出。
            TypeError: 尝试对非list类型的对象进行操作时抛出。
        """
        # WARNING: 注意redis的lrange函数和python的slice的差异，
        #          lrange的右边索引是闭区间，
        #          而slice的右边索引是开区间。
        #          这中间的细微差异让这个方法非常之难测试。
        #          除非你有详细且严谨的测试为基础，否则不要修改这个方法。
        #
        #          至于lindex函数，和python的list[key]行为相同，
        #          这里作为list[key]的get方法。
        try:
            if isinstance(key, slice):
                # 1.EDGE version(get key in server side):
                #
                #if key.start == key.stop != None: return []
                #
                #start = LEFTMOST if key.start == None else key.start
                #stop = RIGHTMOST if key.stop == None else key.stop-1
                #
                #return self._client.lrange(self.name, start, stop)
   
                # 2.SAFE version(get key in client side):
                value = self._client.lrange(self.name, LEFTMOST, RIGHTMOST)[key]
                return map(self._type_case.to_python, value)
            elif key >= len(self):
                raise IndexError
            else:
                value = self._client.lindex(self.name, key)
                return self._type_case.to_python(value)
        except redispy_exception.ResponseError:
            raise TypeError

    def __delitem__(self, key):
        """ 删除指定区间内的列表元素。

        目前只支持以下三种模式：
            del list[:]
            del list[x:]
            del list[:y]
        以下模式不支持：
            del list[index]
            del list[x:y]

        Args:
            key: 一个索引，或一个range。

        Time:
            O(N)

        Raises:
            IndexError: 当key对象不存在，或key超出范围时抛出。
            TypeError: 尝试对非list类型的对象进行操作时抛出。
        """
        # TODO: 想一个漂亮的办法(尽量不写元数据)解决
        #       del list[x:y] 和 del list[index]
        try:
            if isinstance(key, slice):
                # del list[:] --> del all item in list
                if key.start == key.stop == None:
                    # 当ltrim的start > stop时，清空整个列表 
                    self._client.ltrim(self.name, 1, 0)
                # del list[x:] --> keep list[0:x-1]
                elif key.stop == None:
                    self._client.ltrim(self.name, LEFTMOST, key.start-1) 
                # del list[:y] --> keep list[y:-1]
                elif key.start == None:
                    self._client.ltrim(self.name, key.stop, RIGHTMOST)
                # del list[x:y] --> keep list[0:x-1] and list[y:-1]
                else:
                    raise NotImplementedError
            else:
                raise NotImplementedError
        except redispy_exception.ResponseError:
            raise TypeError

    def remove(self, value):
        """ 移除列表中所有值等于value的元素。

        Args:
            value

        Time:
            O(N)

        Returns:
            被移除元素的数量。

        Raises:
            TypeError: 尝试对非list类型的对象进行操作时抛出。
        """
        try:
            value = self._type_case.to_redis(value)
            return self._client.lrem(self.name, value, REMOVE_ALL_ELEMENT_EQUAL_VALUE)
        except redispy_exception.ResponseError:
            raise TypeError

    # TODO: redis2.3将支持push多个值
    def lpush(self, value):
        """ 将value添加到表头。

        Args:
            value: 要添加的值。

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 尝试对非list类型的对象进行操作时抛出。
        """
        try:
            value = self._type_case.to_redis(value)
            self._client.lpush(self.name, value)
        except redispy_exception.ResponseError:
            raise TypeError

    def lpop(self):
        """ 将表头元素弹出。

        Time:
            O(1)

        Returns:
            value: 表头元素。

        Raises:
            IndexError: 对空列表执行操作时抛出。
            TypeError: 尝试对非list类型的对象进行操作时抛出。
        """
        try:
            if len(self) == 0:
                raise IndexError
            value = self._client.lpop(self.name)
            return self._type_case.to_python(value)
        except redispy_exception.ResponseError:
            raise TypeError

    def blpop(self, timeout=INDEFINITELY):
        """ blpop是lpop命令的阻塞版本，
        当给定列表内没有任何元素可供弹出的时候，
        连接将被blpop命令阻塞，直到等待超时或发现可弹出元素为止。 


        Args:
            timeout: 等待的超时时间，0为一直等待。
                     默认为0。

        Returns:
            None: 当等到超时且没有元素被返回时。
            value: 列表不为空。

        Raises:
            TypeError: 尝试对非list类型的对象进行操作时抛出。
        """
        # redis原来的blpop可以对多个key进行blpop，这里只对单个key。
        # 因此，redis原来的返回值格式是(key, value)，
        # 而这里只返回value(原因同上)。
        try:
            result = self._client.blpop(self.name, timeout)

            value = result[VALUE] if result else None

            return self._type_case.to_python(value)
        except redispy_exception.ResponseError:
            raise TypeError

    # TODO: >= 2.4: 接受多个值
    def rpush(self, value):
        """ 将value添加到表尾。

        Args:
            value: 要添加到表尾的项。

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 尝试对非list类型的对象进行操作时抛出。
        """
        try:
            value = self._type_case.to_redis(value) 
            self._client.rpush(self.name, value)
        except redispy_exception.ResponseError:
            raise TypeError

    def rpop(self):
        """ 将表尾元素弹出。

        Time:
            O(1)

        Returns:
            value: 表尾元素

        Raises:
            TypeError: 尝试对非list类型的对象进行操作时抛出。
            IndexError: 对空列表执行操作时抛出。
        """
        try:
            if len(self) == 0:
                raise IndexError
            value = self._client.rpop(self.name)
            return self._type_case.to_python(value)
        except redispy_exception.ResponseError:
            raise TypeError

    def brpop(self, timeout=INDEFINITELY ):
        """ brpop是rpop命令的阻塞版本，
        当给定列表内没有任何元素可供弹出的时候，
        连接将被brpop命令阻塞，直到等待超时或发现可弹出元素为止。 
        
        Args:
            timeout: 等待的超时时间，0为一直等待。
                     默认为0。

        Returns:
            None: 当等到超时且没有元素被返回时。
            value: 列表不为空。

        Raises:
            TypeError: 尝试对非list类型的对象进行操作时抛出。
        """
        # redis原来的brpop可以对多个key进行brpop，这里只对单个key。
        # 因此，redis原来的返回值格式是(key, value)，
        # 而这里只返回value(原因同上)。
        try:
            result = self._client.brpop(self.name, timeout)

            value = result[VALUE] if result else None

            return self._type_case.to_python(value)
        except redispy_exception.ResponseError:
            raise TypeError

    def rpoplpush(self, destination):
        """ 在一个原子时间内，完成以下三件事：
        1.对self进行rpop，
        2.将弹出的元素返回客户端，
        3.将该元素副本lpush到destination。

        Args:
            destination: 另一个列表，或列表名字。

        Time:
            O(1)

        Returns:
            None: 当列表为空时返回。
            value: 当列表不为空时，返回被弹出的元素。

        Raises:
            TypeError: 尝试对非list类型的对象进行操作时抛出。
        """
        try:
            destination = get_key_name_from_single_value(destination)
            value = self._client.rpoplpush(self.name, destination)
            return self._type_case.to_python(value)
        except redispy_exception.ResponseError:
            raise TypeError

    def brpoplpush(self, destination, timeout=INDEFINITELY):
        """ rpoplpush的阻塞版本。
        接受一个timeout参数作为阻塞超时时间。

        Args:
            destination: 另一个列表，或列表名字。
            timeout: 阻塞等待时间，默认为0。

        Time:
            O(1)

        Returns:
            None: 当列表为空时返回。
            value: 当列表不为空时，返回被弹出的元素。

        Raises:
            TypeError: 尝试对非list类型的对象进行操作时抛出。
        """
        try:
            destination = get_key_name_from_single_value(destination)
            value = self._client.brpoplpush(self.name, destination, timeout)
            return self._type_case.to_python(value)
        except redispy_exception.ResponseError:
            raise TypeError
