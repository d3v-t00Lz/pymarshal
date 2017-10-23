"""

"""

import bson
import pytest

from pymarshal.bson import *


def test_marshal_bson():
    class DummyClass:
        _marshal_exclude = ['d']

    _id = bson.ObjectId()

    obj = DummyClass()
    obj._id = _id
    obj.a = DummyClass()
    obj.d = 20  # should not be in output
    obj.a.b = 5
    obj.a.d = 50  # should not be in output

    j = marshal_bson(obj)
    assert j == {'_id': _id, 'a': {'b': 5}}


def test_unmarshal_bson():
    class TestClassA:
        def __init__(self, _id, b):
            self._id = type_assert(_id, bson.ObjectId)
            self.b = type_assert(b, TestClassB)

    class TestClassB:
        def __init__(self, b):
            self.b = type_assert(b, float)

    _id = bson.ObjectId()
    obj = unmarshal_bson(
        {'_id': _id, 'b': {'b': 10.2, 'c': 4.5}}, # 'c' should be ignored
        TestClassA,
    )
    assert obj._id == _id
    assert obj.b.b == 10.2
    assert not hasattr(obj.b, 'c')

