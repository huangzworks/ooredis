# coding: utf-8

def is_any_instance(value, *types):
    """ 接受一个值 value ，以及任意数量的类型 types ，
    如果 value 是 types 中任何一个类型的实例时，返回 True 。
    """
    return any(map(lambda t: isinstance(value, t), types))
