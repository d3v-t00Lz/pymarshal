"""

"""

from pymarshal.util.init_args import init_args

def test_init_args():
    class C:
        def __init__(self, a, b):
            pass

    expected = ('a', 'b')
    assert init_args(C) == expected  # class
    assert init_args(C(1, 2)) == expected  # instance


def test_init_args_factory_function():
    def factory(a, b):
        pass

    expected = ('a', 'b')
    assert init_args(factory) == expected


def test_init_args_factory_method():
    class A:
        def __init__(self, a, b, c):
            pass

        @staticmethod
        def factory(a, b):
            pass

    expected = ('a', 'b')
    assert init_args(A.factory) == expected
