# coding: utf-8

__all__ = ['CommonKeyPropertyMixin']

__metaclass__ = type

class CommonKeyPropertyMixin:

    """
    包含所有 Redis key 通用的操作和属性。
    """

    @property
    def _represent(self):
        """ 
        返回 Key 对象在 Redis 中的表示(底层的实现类型)。

        Args:
            None

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

        Raises:
            None
        """
        return self._client.type(self.name)


    @property
    def ttl(self):
        """ 
        返回 key 的生存时间。

        Args:
            None

        Time:
            O(1)

        Returns: 
            None: key 不存在，或 key 没有设置生存时间。
            ttl_in_second: 以秒为单位的生存时间值。

        Raises:
            None
        """
        return self._client.ttl(self.name)


    @property
    def exists(self):
        """ 
        检查 key 是否存在。

        Args:
            None

        Time:
            O(1)

        Returns:
            bool: key 存在返回 True ，否则为 False 。

        Raises:
            None
        """
        return self._client.exists(self.name)


    def delete(self):
        """ 
        删除 key 。

        Args:
            None

        Time:
            O(1)

        Returns:
            None

        Raises:
            None
        """
        self._client.delete(self.name)


    def expire(self, second):
        """ 
        为 key 设置生存时间。

        Args:
            second: 以秒为单位的生存时间。

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 尝试对不存在的 key 进行设置时抛出。
        """
        # redis-py 对不存在的 key 进行 expire 时返回false，
        # 这里抛出一个异常。
        if not self.exists:
            raise TypeError

        self._client.expire(self.name, second)


    def expireat(self, unix_timestamp):
        """ 
        为 key 设置生存时间，以一个 unix 时间戳为终止时间。

        Args:
            unix_timestamp: 以 unix 时间戳为格式的生存时间。

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 对一个不存在的 key 进行操作时抛出。
        """
        # redis-py 对不存在的 key 进行 expireat 时返回False，
        # 这里抛出一个异常。
        if not self.exists:
            raise TypeError

        self._client.expireat(self.name, unix_timestamp)


    def persist(self):
        """ 
        移除 key 的生存时间

        Args:
            None

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 对一个不存在的 key 进行操作时抛出
        """
        # redis-py 对不存在的 key 进行 persist 返回-1
        # 这里抛出一个异常
        if not self.exists:
            raise TypeError

        self._client.persist(self.name)
