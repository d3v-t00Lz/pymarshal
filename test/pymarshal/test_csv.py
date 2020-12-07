from pymarshal.csv import *
import pytest


def test_marshal_unmarshal_list():
    class Test:
        def __init__(self, a, b):
            self.a = a
            self.b = b

    u = [Test("a", 2), Test("b", 3)]
    assert u[0].a == "a", u[0].a
    m = marshal_csv(u)
    assert m[0][0] == "a", m[0][0]
    u = unmarshal_csv_list(m, Test)
    assert u[0].a == "a", u[0].a

def test__marshal_list_row_header():
    class Test:
        _marshal_list_row_header = "abc"
        def __init__(self, a, b):
            self.a = a
            self.b = b

    u = [Test("a", 2), Test("b", 3)]
    m = marshal_csv(u)
    assert m == [["abc", "a", 2], ["abc", "b", 3]], m

def test_unmarshal_csv():
    class A:
        _marshal_list_row_header = "a"
        def __init__(self, a, b):
            self.a = a
            self.b = b

    class B:
        def __init__(self, a, b):
            self.a = a
            self.b = b

    class C:
        _marshal_list_row_header = "c"
        def __init__(self, a, b):
            self.a = a
            self.b = b

    class D:
        _unmarshal_csv_map = {'a': {'arg_name': 'a', 'type': A}}
        _unmarshal_csv_default_arg = {'arg_name': 'b', 'type': B}
        _unmarshal_csv_singletons = {'c': {'arg_name': 'c', 'type': C}}
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c
        def __iter__(self):
            for x in self.a:
                yield x
            for x in self.b:
                yield x
            yield self.c

    d = D([A(1, 2)], [B(3, 4)], C(5, 6))
    m = marshal_csv(d)
    u = unmarshal_csv(m, D)
    assert u.a[0].a == 1, u.a[0]

def test_unmarshal_csv_raises_attribute_error():
    class A:
        pass
    with pytest.raises(AttributeError):
        unmarshal_csv([], A)

def test_unmarshal_csv_raises_value_error():
    class A:
        _unmarshal_csv_map = {
            'a': {'arg_name': 'a', 'type': object},
        }
        def __init__(self, a):
            self.a = a

    with pytest.raises(ValueError):
        unmarshal_csv([[1, 2]], A)

