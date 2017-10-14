"""

"""

from pymarshal import *


def test_marshal_json():
    class DummyClass:
        pass

    obj = DummyClass()
    obj.a = DummyClass()
    obj.a.b = 5

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

