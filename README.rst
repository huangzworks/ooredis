OOREDIS
=======

OORedis 是一个 Redis 的 Python 库，它基于 redis-py ，具有以下三个主要功能：

- 以 Key 对象为单位操作 Redis 的数据结构
- 提供一组 Pythonic 的 API
- 提供方便的类型转换机制 


用例
------

::

    >>> from ooredis import *
    >>> connect()
    >>>
    >>> project = Dict('project-info')
    >>> project['name'] = 'OORedis'
    >>> project['description'] = 'A Python-to-Redis mapper'
    >>> project['language'] = 'Python'
    >>> project.items()
    [('name', 'OORedis'),  ('description', 'A Python-to-Redis mapper'), ('language', 'Python')]
    >>>
    >>> book_list = Deque('my-book-list')
    >>> book_list.append('SICP')
    >>> book_list.append('The Joy of Clojure')
    >>> book_list.append('Real World Haskell')
    >>> list(book_list)
    ['SICP', 'The Joy of Clojure', 'Real World Haskell']
    >>> book_list.pop()
    'Real World Haskell'
    >>>
    >>> my_friend = Set('my-friend')
    >>> my_friend.add('peter')
    >>> my_friend.add('jack')
    >>> my_friend.add('mary')
    >>> your_friend = set(['peter', 'bob', 'yui'])
    >>> my_friend ^ your_friend
    set(['yui', 'bob', 'mary', 'jack'])
    >>> my_friend & your_friend
    set(['peter'])
    >>> my_friend
    Set Key 'my-friend': set(['peter', 'mary', 'jack'])
    >>> my_friend &= your_friend
    >>> my_friend
    Set Key 'my-friend': set(['peter'])
    >>>
    >>> price = SortedSet('fruit-price')
    >>> price['apple'] = 6.5
    >>> price['banana'] = 3.2
    >>> price['cherry'] = 4
    >>> price
    Sortedset Key 'fruit-price': [{'score': 3.2, 'value': 'banana'}, {'score': 4.0, 'value': 'cherry'}, {'score': 6.5, 'value': 'apple'}]
    >>> for p in price:
    ...     print(p)
    ... 
    {'score': 3.2, 'value': 'banana'}
    {'score': 4.0, 'value': 'cherry'}
    {'score': 6.5, 'value': 'apple'}
    >>> for p in reversed(price):
    ...     print(p)
    ... 
    {'score': 6.5, 'value': 'apple'}
    {'score': 4.0, 'value': 'cherry'}
    {'score': 3.2, 'value': 'banana'}


文档
------

更多代码示例和具体用法，请参考在线文档： `http://ooredis.readthedocs.org/ <http://ooredis.readthedocs.org/>`_ 


测试
------

注意：\ **测试将清空 Redis 的 0 号数据库**\ ，请谨慎操作。

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
------

本软件由 huangz 编写，
你可以在免费且自由的情况下，下载、使用、修改本软件，如果你需要其他许可，
请使用以下方式与我取得联系：

twitter: `@huangz1990 <https://twitter.com/huangz1990>`_

gmail: huangz1990

豆瓣: `www.douban.com/people/i_m_huangz <http://www.douban.com/people/i_m_huangz/>`_
