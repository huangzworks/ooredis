# coding: utf-8

__all__ = ['String']

__metaclass__ = type

from helper import format_key
from base_key import BaseKey
from common_key_property_mixin import CommonKeyPropertyMixin
from set_and_get_op_mixin import SetAndGetOpMixin

class String(BaseKey, CommonKeyPropertyMixin, SetAndGetOpMixin):

    """
    为储存单个值的 Key 对象提供 set，get 和 getset 等操作。
    """

    def __repr__(self):
        return format_key(self, self.name, self.get())
