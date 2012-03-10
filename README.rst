OOREDIS
=======

OORedis 是一个 Redis 的 Python 库，它基于 redis-py ，具有以下三个主要功能：

- 以 Key 对象为单位操作 Redis 的数据结构
- 提供一组 Pythonic 的 API
- 提供方便的类型转换机制 


需求
====

Python2.7

Redis2.2

redis-py2.4.9

nosetest(用于测试)


安装
====

::

    $ sudo pip2 install ooredis
    Downloading/unpacking ooredis
    Downloading ooredis-1.0.tar.gz
    Running setup.py egg_info for package ooredis
    
    Installing collected packages: ooredis
    Running setup.py install for ooredis
                    
    Successfully installed ooredis
    Cleaning up...
    
    $ python2
    Python 2.7.2 (default, Jun 29 2011, 11:17:09) 
    [GCC 4.6.1] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import ooredis
    >>> 


示例
=====

::

    >>> from ooredis import *
    >>> dir()
    ['Counter', 'Dict', 'List', 'Set', 'SingleValue', 'SortedSet', '__builtins__', '__doc__', '__name__', '__package__', 'connect', 'get_client', 'type_case']
    >>>
    >>> connect(db=1)   
    <redis.client.Redis object at 0xb71cae4c>
    >>>
    >>> project = Dict('ooredis')
    >>> project['name'] = 'ooredis'
    >>> project['version'] = 1.0
    >>> project['author'] = 'huangz'
    >>> 
    >>> friends = Set('my_friends')
    >>> friends.add('marry')
    >>> friends.add('jack')
    >>> set(friends)
    set([u'marry', u'jack'])
    >>> 
    >>> 
    
    
简介
====

关于更多代码示例及说明，请参见以下幻灯：
(推荐翻墙使用 google doc 观看，因为幻灯在 slideshare 显示有排版错误)

`去 slideshare 观看 <http://www.slideshare.net/iammutex/ooredis-8792195>`_

`去 google docs 观看 <http://bit.ly/rbgn3Z>`_


文档
====

OORedis 代码中内置了函数的基本介绍，可以使用 ``help(obj)`` 来查看

::

    >>> from ooredis import Set
    >>> help(Set)
    >>>
    Help on class Set in module ooredis.mix.set:
    
    class Set(ooredis.mix.key.Key)
    |  集合类型，底层实现是redis的set类型。
    |  
    |  Method resolution order:
    |      Set
    |      ooredis.mix.key.Key
    |      __builtin__.object
    |  
    |  Methods defined here:
    |  
    |  __and__(self, other)
    |      __and__的反向方法，用于支持多集合进行交集操作。
    |  
    |  __contains__(self, element)
    |      查元素element是否是集合的成员。
    |      
    |      Args:
    |          element
    |      
    |      Time:
    |          O(1)
    |...
    
    
测试
====

注意：\ **测试将清空Redis的0号数据库**\ ，请谨慎操作。

::

    $ git clone git://github.com/huangz1990/ooredis.git
    Cloning into ooredis...
    remote: Counting objects: 112, done.
    remote: Compressing objects: 100% (81/81), done.
    remote: Total 112 (delta 38), reused 102 (delta 28)
    Receiving objects: 100% (112/112), 68.03 KiB | 44 KiB/s, done.
    Resolving deltas: 100% (38/38), done.
    $ cd ooredis/
    $ nosetests
    .................................................................................................................................................................................................................................................................................................................................
    ----------------------------------------------------------------------
    Ran 321 tests in 5.803s

    OK


许可
=====

你可以在免费且自由的情况下，下载、使用、修改本软件，如果你需要其他许可，请联系作者。


联系方式
========

twitter: `@huangz1990 <https://twitter.com/huangz1990>`_

gmail: huangz1990

豆瓣: `www.douban.com/people/i_m_huangz <http://www.douban.com/people/i_m_huangz/>`_
