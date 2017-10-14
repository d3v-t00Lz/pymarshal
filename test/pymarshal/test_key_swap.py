"""

"""

from pymarshal.key_swap import key_swap

def test_key_swap():
    class TestClass:
        _unmarshal_key_swap = {
            'a': 'A',
        }
        _marshal_key_swap = {
            'A': 'a',
        }
    for d, m, expected in [
        ({'a': 5}, False, {'A': 5}),
        ({'A': 5}, True, {'a': 5}),
    ]:
        obj = key_swap(d, TestClass, m)
        assert obj == expected

