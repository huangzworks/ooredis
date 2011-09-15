# coding: utf-8

<<<<<<< HEAD
__all__ = ['Server']

__metaclass__ = type

=======
>>>>>>> 278bbcea2a47ef2663ccab1b46853c183b3830d8
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
