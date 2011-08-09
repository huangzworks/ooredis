# coding: utf-8

# redis的数据类型
REDIS_TYPE = {
    'string': 'string',
    'list': 'list',
    'hash': 'hash',
    'set': 'set',
    'sorted_set': 'zset',
    'not_exists': 'none',
}

# redis列表和有序集的range边界
LEFTMOST = 0
RIGHTMOST = -1

# 默认增量和减量
DEFAULT_INCREMENT = DEFAULT_DECREMENT = 1
