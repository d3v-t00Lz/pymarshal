"""

"""

import pytest

from pymarshal import *


def test_marshal_json():
    class DummyClass:
        _marshal_exclude = ['d']

    obj = DummyClass()
    obj.a = DummyClass()
    obj.d = 20  # should not be in output
    obj.a.b = 5
    obj.a.d = 50  # should not be in output

    j = marshal_json(obj)
    assert j == {'a': {'b': 5}}


def test_unmarshal_json():
    class TestClassA:
        def __init__(self, a, b):
            self.a = type_assert(a, int)
            self.b = type_assert(b, TestClassB)

    class TestClassB:
        def __init__(self, b):
            self.b = type_assert(b, float)


    obj = unmarshal_json({'a': 5, 'b': {'b': 10.2}}, TestClassA)
    assert obj.a == 5
    assert obj.b.b == 10.2


def test_unmarshal_json_raises_extra_keys_error():
    class TestClassA:
        def __init__(self, a):
            self.a = type_assert(a, int)

    with pytest.raises(ExtraKeysError):
        unmarshal_json(
            {'a': 5, 'b': 2},
            TestClassA,
            allow_extra_keys=False,
        )

def test_unmarshal_json_allow_extra_keys():
    class TestClassA:
        def __init__(self, a):
            self.a = type_assert(a, int)

    obj = unmarshal_json(
        {'a': 5, 'b': 2},
        TestClassA,
        allow_extra_keys=True,
    )

    assert obj.a == 5
    assert not hasattr(obj, 'b')

