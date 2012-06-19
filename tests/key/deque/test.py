# coding: utf-8

from redis import Redis
from ooredis import Deque
from unittest import TestCase

from ooredis.key.helper import format_key
from ooredis.type_case import IntTypeCase

class TestDeque(TestCase):

    def setUp(self):
        self.redispy = Redis()

        self.item = 10086 
        self.another_item = 10000

        self.multi_item = [123, 321, 231]

        self.d = Deque('deque', type_case=IntTypeCase)
   
    def tearDown(self):
        self.redispy.flushdb()

    # helper

    def set_wrong_type(self, key_object):
        self.redispy.set(key_object.name, 'string')

    # __repr__

    def test__repr__(self):
        assert repr(self.d) == format_key(self.d, self.d.name, list(self.d))

    # __len__

    def test_len_when_EMPTY(self):
        assert len(self.d) == 0

    def test_len_when_NOT_EMPTY(self):
        self.d.append(self.item)
        assert len(self.d) == 1
    
    def test_len_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            len(self.d)

    # append

    def test_append_when_EMPTY(self):
        self.d.append(self.item)

        assert list(self.d) == [self.item]
        assert len(self.d) == 1

    def test_append_when_NOT_EMPTY(self):
        self.d.append(self.item)
        self.d.append(self.another_item)

        assert list(self.d) == [self.item, self.another_item]
        assert len(self.d) == 2

    def test_append_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            self.d.append(self.item)

    # extend

    def test_extend_when_EMPTY(self):
        self.d.extend(self.multi_item)

        assert list(self.d) == self.multi_item
        assert len(self.d) == len(self.multi_item)

    def test_extend_when_NOT_EMPTY(self):
        self.d.extend(self.multi_item)

        self.d.extend(self.multi_item)

        assert list(self.d) == self.multi_item * 2
        assert len(self.d) == len(self.multi_item) * 2

    def test_extend_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            self.d.extend(self.multi_item)

    # extendleft

    def test_extendleft_when_EMPTY(self):
        self.d.extendleft(self.multi_item)

        assert list(self.d) == list(reversed(self.multi_item))
        assert len(self.d) == len(self.multi_item)

    def test_extendleft_when_NOT_EMPTY(self):
        self.d.extendleft(self.multi_item)
        
        self.d.extendleft(self.multi_item)

        assert list(self.d) == list(reversed(self.multi_item)) * 2
        assert len(self.d) == len(self.multi_item) * 2

    def test_extend_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            self.d.extendleft(self.multi_item)

    # appendleft

    def test_appendleft_when_EMPTY(self):
        self.d.appendleft(self.item)

        assert list(self.d) == [self.item]
        assert len(self.d) == 1

    def test_appendleft_when_NOT_EMPTY(self):
        self.d.appendleft(self.item)
        self.d.appendleft(self.another_item)

        assert list(self.d) == [self.another_item, self.item]
        assert len(self.d) == 2

    def test_append_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            self.d.appendleft(self.item)

    # __iter__

    def test__iter__when_EMPTY(self):
        assert list(self.d) == []

    def test__iter__when_NOT_EMPTY(self):
        self.d.append(self.item)
        assert list(self.d) == [self.item]

    def test__iter__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            list(self.d)

    # clear

    def test_clear_when_EMPTY(self):
        self.d.clear()
        assert list(self.d) == []
        assert len(self.d) == 0

    def test_clear_when_NOT_EMPTY(self):
        self.d.append(self.item)

        self.d.clear()

        assert list(self.d) == []
        assert len(self.d) == 0

    # count

    def test_count_when_EMPTY(self):
        assert self.d.count(self.item) == 0

    def test_count_when_NOT_EMPTY_and_ITEM_FOUNDED(self):
        self.d.append(self.item)
        assert self.d.count(self.item) == 1

        self.d.append(self.item)
        assert self.d.count(self.item) == 2

        self.d.append(self.another_item)
        assert self.d.count(self.item) == 2

    def test_count_when_NOT_EMPTY_and_ITEM_NOT_FOUND(self):
        self.d.append(self.item)
        assert self.d.count(self.another_item) == 0

    def test_count_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            self.d.count(self.item)

    # pop

    def test_pop_RAISE_when_EMPTY(self):
        with self.assertRaises(IndexError):
            self.d.pop()

    def test_pop_with_SINGLE_ITEM(self):
        self.d.append(self.item)

        assert self.d.pop() == self.item
        assert len(self.d) == 0

    def test_pop_with_MULTI_ITEM(self):
        self.d.append(self.item)
        self.d.append(self.another_item)

        assert self.d.pop() == self.another_item
        assert len(self.d) == 1

    def test_pop_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            self.d.pop()


    # block_pop

    def test_block_pop_RETURN_NONE_when_EMPTY(self):
        self.assertIsNone(
            self.d.block_pop(1)
        )

    def test_block_pop_with_SINGLE_ITEM(self):
        self.d.append(self.item)

        self.assertEqual(
            self.d.block_pop(1),
            self.item
        )

        self.assertEqual(
            len(self.d),
            0
        )

    def test_block_pop_with_MULTI_ITEM(self):
        self.d.append(self.item)
        self.d.append(self.another_item)

        self.assertEqual(
            self.d.block_pop(),
            self.another_item
        )

        self.assertEqual(
            len(self.d),
            1
        )

    def test_pop_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            self.d.block_pop()


    # popleft

    def test_popleft_RAISE_when_EMPTY(self):
        with self.assertRaises(IndexError):
            self.d.popleft()

    def test_popleft_with_SINGLE_ITEM(self):
        self.d.appendleft(self.item)

        assert self.d.popleft() == self.item
        assert len(self.d) == 0

    def test_popleft_with_MULTI_ITEM(self):
        self.d.appendleft(self.item)
        self.d.appendleft(self.another_item)

        assert self.d.popleft() == self.another_item
        assert len(self.d) == 1

    def test_popleft_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            self.d.popleft()


    # block_popleft

    def test_block_popleft_RETURN_NONE_when_DEQUE_EMPTY(self):
        self.assertIsNone(
            self.d.block_popleft(1)
        )

    def test_block_popleft_with_SINGLE_ITEM(self):
        self.d.appendleft(self.item)

        self.assertEqual(
            self.d.block_popleft(1),
            self.item
        )

        self.assertEqual(
            len(self.d),
            0
        )

    def test_block_popleft_with_MULTI_ITEM(self):
        self.d.appendleft(self.item)
        self.d.appendleft(self.another_item)

        self.assertEqual(
            self.d.block_popleft(1),
            self.another_item
        )

        self.assertEqual(
            len(self.d),
            1
        )

    def test_block_popleft_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            self.d.block_popleft()


    # __getitem__

    def test__getitem__use_INDEX(self):
        self.d.append(self.item)
        assert self.d[0] == self.item

    def test__getitem__RAISE_when_OUT_OF_INDEX(self):
        with self.assertRaises(IndexError):
            self.d[10086]

    def test__getitem__use_SLICE(self):
        for i in range(5):
            self.d.append(self.item)
        assert self.d[:5] == [self.item] * 5

    def test__getitem__RETURN_EMPTY_LIST_when_OUT_OF_RANGE(self):
        assert self.d[123:10086] == [] 
    
    def test__getitem__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            self.d[0]

    """
    # __delitem__

    def test__delitem__DELETE_ALL_ITEM_when_EMPTY(self):
        del self.d[:]
        assert list(self.d) == []

    def test__delitem__DELETE_ALL_ITEM_with_SINGLE_ITEM(self):
        self.d.append(self.item)

        del self.d[:]
        assert list(self.d) == []

    def test__delitem__DELETE_ALL_ITEM_with_MULTI_ITEM(self):
        self.d.append(self.multi_item)

        del self.d[:]
        assert list(self.d) == []

    # use left range

    def test__delitem__given_LEFT_RANGE(self):
        self.d.append(self.multi_item)

        del self.d[1:]
        self.assertEqual(list(self.d), list(self.multi_item[0]))
        assert list(self.d) == list(self.multi_item[0])

    # use index

    def test__delitem__by_INDEX_RAISE_when_OUT_OF_INDEX(self):
        with self.assertRaises(IndexError):
            del self.d[10086]

    def test__delitem__by_INDEX_with_SINGLE_ITEM(self):
        self.d.append(self.item)

        del self.d[0]
        assert list(self.d) == []

    def test__delitem__by_INDEX_with_MULTI_ITEM(self):
        self.d.append(self.multi_item)

        del self.d[0]
        assert list(self.d) == self.multi_item[1:]

    # wrong type

    def test__delitem__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.d)
            del self.d[:]
    """
