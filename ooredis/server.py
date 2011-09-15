# coding: utf-8

__all__ = ['Server']

__metaclass__ = type

from ooredis import get_client

class Server:
    """ Redis的Server相关命令包装。 """

    @staticmethod
    def flushdb(client=get_client()):
        """ 清除当前数据库的所有key。

        Args:
            client: redis-py句柄

        Time:
            O(1)

        Return:
            None
        """
        client.flushdb()
