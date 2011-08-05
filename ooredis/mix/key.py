# coding:utf-8

__all__ = ['Key']

__metaclass__ = type

from ooredis.client import get_client
from ooredis.type_case import GenericTypeCase

class Key:
    """ key对象的基类，所有类型的key都继承这个类。 """

    def __init__(self, name, client=None, type_case=None):
        """ 为key对象指定名字和客户端。

        Args:
            name: key的名字
            client: 客户端，默认为全局客户端。
        """
        self._client = client or get_client()
        self._name = name
        self._type_case = type_case or GenericTypeCase

    def __eq__(self, other):
        """ 判断两个key是否相等。

        Args:
            other: 另一个key对象。

        Time:
            O(1)

        Returns:
            bool
        """
        return self.name == other.name

    def __str__(self):
        """ 为key对象创建一个酷酷的打印信息。 """
        key_type = self.__class__.__name__
        return "<{0} Key '{1}'>".format(key_type.title(), self.name)

    @property
    def name(self):
        """ 返回key对象的名字。 """
        return self._name

    @property
    def _represent(self):
        """ 返回key在redis中的表示(实现类型)。

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
        """ 返回key的生存时间。

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
        """ 检查key是否存在。

        Time:
            O(1)

        Returns:
            bool: key存在返回True，否则为False。
        """
        return self._client.exists(self.name)

    # TODO: 这个delete只能删除单个key，
    #       考虑增加一个删除多个key的类方法
    def delete(self):
        """ 删除key。


        Time:
            O(1)

        Returns:
            None

        Raises:
            AssertionError: 操作因为异常情况而失败时抛出。
        """
        # redis-py里，对不存在的key进行删除返回False， 删除成功返回True，
        # 这里只删除存在的key，返回None，如果出现问题导致删除失败，抛出异常。
        if self.exists:
            assert(self._client.delete(self.name))

    def expire(self, second):
        """ 为key设置生存时间
        
        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 尝试对不存在的key进行设置时抛出。
            AssertionError: 操作因为异常情况而失败时抛出。
        """
        # redis-py对不存在的key进行expire返回false，
        # 这里抛出一个异常。
        if self.exists == False:
            raise TypeError

        assert(self._client.expire(self.name, second))

    def expireat(self, unix_timestamp):
        """ 为key设置生存时间，以一个unix时间戳为终止时间。

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 对一个不存在的key进行操作时抛出。
            AssertionError: 操作因为异常情况而失败时抛出。
        """
        # redis-py对不存在的key进行expireat返回False，
        # 这里抛出一个异常。
        if self.exists == False:
            raise TypeError

        assert(self._client.expireat(self.name, unix_timestamp))

    def persist(self):
        """ 移除key的生存时间

        Time:
            O(1)

        Returns:
            None

        Raises:
            TypeError: 对一个不存在的key进行操作时抛出
            AssertionError: 操作因为异常情况而失败时抛出
        """
        # redis-py对不存在的key进行persist返回-1
        # 这里抛出一个异常
        if self.exists == False:
            raise TypeError

        # redis-py对没有生存时间的key进行persist也返回-1
        # 这里选择不进行其他动作(返回None)
        if self.ttl == None:
            return

        assert(self._client.persist(self.name))


# TODO:
class SortableKey:
    """ 为可排序的key提供sort方法。 """

    def sort(self, *args, **kwargs):
        # TODO: ...
        raise NotImplementedError

    def sortget(self, value):
        """ sort方法的一个hack，相当于外键来使用，可以获取多个外键。

        将
        >>> r.sort('user_id', by='not_exists_key', get=('#', 'user_name_*', 'user_password_*') 
        >>> ['222', 'hacker', 'hey,im in', '59230', 'jack', 'jack201022', '2', 'huangz', 'nobodyknows', '1', 'admin', 'a_long_long_password']
        
        改成
        >>> Key('user_id').get('#', 'user_name_*', 'user_password_*')

        或
        >>> Key('user_id').get('#').get('user_name_*').get('user_password_*')

        以及limit
        >>> Key('user_id').get('#').get('user_name_*').get('user_password_*').skip(skip_num).count(count_num)

        列出前10条，key.get() == key.get('#')
        >>> Key('user_id').get().get('user_name_*').get('user_password_*').skip(0).count(10)


        这个方法虽然很cool，但是GET只支持key级别操作，似乎实际效果不是很大。
        """
        pass


# helper

def get_key_name_from_single_value(value):
    """ 从单个值中获取key对象的名字。 """
    return value.name if isinstance(value, Key) else value
   
def get_key_name_from_list(iterable):
    """ 从列表/元组中获取多个key对象的名字。 """
    return map(get_key_name_from_single_value, iterable)
