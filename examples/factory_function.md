```python
# Example of how to avoid putting logic into __init__ using
# the 'factory' design pattern.  Also demonstrates the use of
# dependency injection.

from pymarshal.json import *

def complex_constructor_factory(
    a_start=50,
    a_end=60,
    b_start=100,
    b_end=110,
):
    """ Nonsensical example, returns a ComplexConstructor instance.

        Using this design pattern keeps the logic out of __init__,
        to facilitate unmarshalling using PyMarshal,
        with the added benefit of making your code easier to unit test
    """
    a = list(range(a_start, a_end))
    b = list(range(b_start, b_end))
    return ComplexConstructor(a, b)


class ComplexConstructor:
    """ Nonsensical class """
    def __init__(self, a, b):
        """
        Args:
            a: list-of-int, some list of integers
            b: list-of-int, some list of integers
        """
        self.a = type_assert_iter(a, int)
        self.b = type_assert_iter(b, int)
```
