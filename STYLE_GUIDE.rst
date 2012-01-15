OOREDIS风格指南
******************

注释风格
============

OORedis 的注释遵循 `Google Python Style Guide <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html>`_ 。

**类注释模板：**

::

    class AnotherClass:
        """ 类注释 """

        def method(self, arg1, arg2, ...):
            """ 方法简要说明
            
            Args:
                arg1: 对参数1的说明
                arg2: 对参数2的说明

            Time:
                方法的算法时间复杂度

            Returns:
                返回值的类型: 对返回值的说明

            Raises:
                抛出的异常: 抛出异常的情况说明
            """
            # 一些针对编程人员的注释
            pass

**示例：**

::

    class List(Key, collections.Sequence):
        """ 一个列表key对象，底层实现是redis的list类型。 """

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
            # 这个函数是用Reids的llen命令实现的
            pass
    

异常策略
===========

OORedis 抛出异常的策略仿效 Python 内置类的异常抛出策略。

像是 ``ooredis.mix.Dict`` 模仿 ``dict`` 类型，而 ``ooredis.mix.List`` 则模仿 ``list`` 类型。

比如当 ``Dict`` 类的实例 ``d`` 在 ``key`` 不存在的情况下执行 ``d[key]`` ， ``Dict`` 和内置的 ``dict`` 类一样，都是抛出 ``KeyError`` 异常。
