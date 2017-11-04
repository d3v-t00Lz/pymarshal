"""

"""

import bson
import datetime

import pytest

from pymarshal.bson import *


def test_marshal_bson():
    class DummyClass:
        _marshal_exclude = ['d']
        def __init__(self):
            pass

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

class FakeMongoDoc(MongoDocument):
    _marshal_exclude_none = True
    def __init__(
        self,
        a,
        b=None,
        c=None,
        d=None,
        _id=None,
    ):
        self.a = type_assert(a, str)
        self.b = type_assert(
            b,
            datetime.datetime,
            allow_none=True,
        )
        self.c = type_assert(
            c,
            bson.ObjectId,
            allow_none=True,
        )
        self.d = type_assert(
            d,
            FakeMongoDoc,
            allow_none=True,
        )
        self._id = type_assert(
            _id,
            bson.ObjectId,
            allow_none=True,
        )


def test_mongodoc_json_include_id_false():
    _id = bson.ObjectId()
    a = FakeMongoDoc("b", _id=_id)
    assert a.json() == {"a": "b"}


def test_mongodoc_json_include_id_true():
    _id = bson.ObjectId()
    a = FakeMongoDoc("b", _id=_id)
    assert a.json(include_id=True) == {"a": "b", "_id": str(_id)}


def test_mongodoc_json_object_id_fmt_none():
    _id = bson.ObjectId()
    a = FakeMongoDoc("b", c=_id, _id=_id)
    assert a.json(object_id_fmt=None) == {"a": "b"}


def test_mongodoc_json_date_fmt_none():
    _id = bson.ObjectId()
    b = datetime.datetime.utcfromtimestamp(0)
    a = FakeMongoDoc("b", b=b, _id=_id)
    j = a.json(date_fmt=None)
    assert b == datetime.datetime.fromtimestamp(j['b'])


def test_mongodoc_json_date_fmt_str():
    _id = bson.ObjectId()
    b = datetime.datetime.utcfromtimestamp(0)
    a = FakeMongoDoc("b", b=b, _id=_id)
    j = a.json(date_fmt='%Y')
    assert j['b'] == '1970'


def test_mongodoc_nested():
    d = FakeMongoDoc(
        'a',
        d=FakeMongoDoc('b'),
    )
    j = d.json()
    assert j['d']['a'] == 'b'

