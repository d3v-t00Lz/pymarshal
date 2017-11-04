"""

"""

import pytest

from pymarshal.json import *


def test_marshal_json():
    class DummyClass:
        _marshal_exclude = ['d']
        def __init__(self):
            pass

    obj = DummyClass()
    obj.a = DummyClass()
    obj.d = 20  # should not be in output
    obj.a.b = 5
    obj.a.d = 50  # should not be in output

    j = marshal_json(obj)
    assert j == {'a': {'b': 5}}


def test_marshal_json_marshal_only_init_args_true():
    class DummyClass:
        _marshal_only_init_args = True
        def __init__(self, a):
            self.a = a
            self.b = 50 # should be ignored

    obj = DummyClass(10)
    j = marshal_json(obj)
    assert j == {'a': 10}


def test_marshal_json_marshal_exclude_none():
    class DummyClass:
        _marshal_exclude_none = True
        def __init__(self, a):
            self.a = a
            self.b = None # should be ignored

    obj = DummyClass(10)
    j = marshal_json(obj)
    assert j == {'a': 10}


def test_marshal_json_marshal_exclude_none_keys():
    class DummyClass:
        _marshal_exclude_none_keys = [
            'b',
        ]
        def __init__(self, a):
            self.a = a
            self.b = None # should be ignored
            self.c = None

    obj = DummyClass(10)
    j = marshal_json(obj)
    assert j == {'a': 10, 'c': None}


def test_unmarshal_json():
    class TestClassA:
        def __init__(self, a, b):
            self.a = type_assert(a, int)
            self.b = type_assert(b, TestClassB)

    class TestClassB:
        def __init__(self, b):
            self.b = type_assert(b, float)


    obj = unmarshal_json(
        {'a': 5, 'b': {'b': 10.2, 'c': 4.5}}, # 'c' should be ignored
        TestClassA,
    )
    assert obj.a == 5
    assert obj.b.b == 10.2
    assert not hasattr(obj.b, 'c')


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


def test_unmarshal_json_raises_extra_keys_error_from_cls():
    class TestClassA:
        def __init__(self, a, b):
            self.a = type_assert(a, int)
            self.b = type_assert(b, TestClassB)

    class TestClassB:
        _unmarshal_allow_extra_keys = False

        def __init__(self, c):
            self.c = type_assert(c, float)

    with pytest.raises(ExtraKeysError):
        unmarshal_json(
            {'a': 5, 'b': {'c': 4.5, 'd': 2.4}},
            TestClassA,
            allow_extra_keys=True,
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


def test_unmarshal_json_factory_function():
    class TestClassA:
        def __init__(self, a, b):
            self.a = type_assert(a, str)
            self.b = type_assert(b, str)

    def factory(a, b):
        return TestClassA(
            str(a),
            str(b),
        )

    t = unmarshal_json({'a': 1, 'b': 2}, factory)
    assert t.a == '1'
    assert t.b == '2'

