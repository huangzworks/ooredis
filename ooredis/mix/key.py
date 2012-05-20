# coding:utf-8

__all__ = ['Key']

__metaclass__ = type

from ooredis.client import get_client
from ooredis.type_case import GenericTypeCase

class Key:

    """ key对象的基类，所有类型的key都继承这个类。 """

    def __init__(self, name, client=None, type_case=GenericTypeCase):
        """ 
        为key对象指定名字和客户端。

        Args:
            name: key的名字
            client: 客户端，默认为全局客户端。
        """
        self.name = name
        self._client = client or get_client()
        self._type_case = type_case

    def __eq__(self, other):
        """ 
        判断两个key是否相等。

        Args:
            other: 另一个key对象。

        Time:
            O(1)

        Returns:
            bool
        """
        return self.name == other.name

    @property
    def _represent(self):
        """ 
        返回key在redis中的表示(实现类型)。

        Time:
            O(1)

        Returns: 
            redis的类型定义在REDIS_TYPE常量中，包含以下：
            'none' : 值不存在
            'string' : 字符串
            'list' : 列表
            'set' : 集合
            'zset' : 有序集
            'hash' : 哈希表
        """
        return self._client.type(self.name)

    @property
    def ttl(self):
        """ 
        返回key的生存时间。

        Time:
            O(1)

        Returns: 
            None: 值不存在，或值没有设置生存时间。
            long: 以秒为单位的生存时间值。
        """
        # NOTE: py3.0之后整数只有int类型了
        return self._client.ttl(self.name)

    @property
    def exists(self):
        """ 
        检查key是否存在。

        Time:
            O(1)

        Returns:
            bool: key存在返回True，否则为False。
        """
        return self._client.exists(self.name)

    def delete(self):
        """ 
        删除key。

        Time:
            O(1)

        Returns:
            None

        Raises:
            None
        """
        if self.exists:
            self._client.delete(self.name)

    def expire(self, second):
        """ 
        为key设置生存时间
        
        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 尝试对不存在的key进行设置时抛出。
        """
        # redis-py对不存在的key进行expire返回false，
        # 这里抛出一个异常。
        if not self.exists:
            raise TypeError

        self._client.expire(self.name, second)

    def expireat(self, unix_timestamp):
        """ 
        为key设置生存时间，以一个unix时间戳为终止时间。

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 对一个不存在的key进行操作时抛出。
        """
        # redis-py对不存在的key进行expireat返回False，
        # 这里抛出一个异常。
        if not self.exists:
            raise TypeError

        self._client.expireat(self.name, unix_timestamp)

    def persist(self):
        """ 
        移除key的生存时间

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 对一个不存在的key进行操作时抛出
        """
        # redis-py对不存在的key进行persist返回-1
        # 这里抛出一个异常
        if not self.exists:
            raise TypeError

        # redis-py对没有生存时间的key进行persist也返回-1
        # 这里选择不进行其他动作(返回None)
        if self.ttl is None:
            return

        self._client.persist(self.name)
