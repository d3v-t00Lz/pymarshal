"""

"""

from pymarshal.init_args import init_args

def test_init_args():
    class C:
        def __init__(self, a, b):
            pass

    expected = ['a', 'b']
    assert init_args(C) == expected  # class
    assert init_args(C(1, 2)) == expected  # instance

