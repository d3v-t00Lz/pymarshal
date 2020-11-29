from pymarshal.util.marshal import *
import pytest


def test_marshal_list_invalid_fields():
    class Test:
        def __init__(self, a):
            self.a = a

    t = Test("123")
    with pytest.raises(ValueError):
        m = marshal_list(t, types=(int,))

def test_unmarshal_list_invalid_fields():
    class Test:
        def __init__(self, a):
            self.a = a

    t = [1, 3, 6, "test"]
    with pytest.raises(InitArgsError):
        m = unmarshal_list(t, Test)

def test_unmarshal_list_dict_cls():
    class Test:
        _marshal_list_row_header = 'zz'
        def __init__(self, a):
            self.a = a
    cls = {
        'zz': Test,
    }
    t = ['zz', 1]
    m = unmarshal_list(t, cls)
    assert m.a == 1, m.a

