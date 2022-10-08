```python
# Example of how to avoid putting logic into __init__ using
# the 'factory' design pattern.  Also demonstrates the use of
# dependency injection.

from pymarshal.json import *


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

    @staticmethod
    def factory(
        a_start=50,
        a_end=60,
        b_start=100,
        b_end=110,
    ):
        """ Constructs a complex object that needs more than field assignment

            You could, of course, have more than one factory method
        """
        a = list(range(a_start, a_end))
        b = list(range(b_start, b_end))
        return ComplexConstructor(a, b)

>>> cc = ComplexConstructor.factory(0, 2, 5, 7)
>>> cc.a
[0, 1]
>>> cc.b
[5, 6]
>>> j =  marshal_json(cc)
>>> j
{'a': [0, 1], 'b': [5, 6]}
>>> # Typically unmarshal should not use the factory method or function,
>>> # except in special cases where you are deliberately transforming data
>>> # from other sources that will not be converted back to the original format
>>> cc2 = unmarshal_json(j, ComplexConstructor)
```
