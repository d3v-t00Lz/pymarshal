"""

"""

from pymarshal.key_swap import key_swap

def test_key_swap():
    class TestClass:
        _pm_key_swap = {
            'a': 'A',
        }
    obj = key_swap({'a': 5}, TestClass)
    assert obj == {'A': 5}

