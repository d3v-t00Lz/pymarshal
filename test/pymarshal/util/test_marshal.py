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
