## Using __slots__

PyMarshal has support for the Python `__slots__` feature that enables
using a class as a `struct`, rather than a `dict`.  This can greatly
improve memory consumption and performance of getting or setting
class members.  This makes Python's performance and memory consumption
directly comparable to Go.

```python
from pymarshal.json import *

class MySlotClass:
    # Must align with every argument to __init__
    __slots__ = [
        'a',
        'b',
    ]

    # There cannot be any extra arguments not defined in __slots__
    def __init__(self, a, b):
        self.a = type_assert(a, int)
        self.b = type_assert(b, str)

# marshal and unmarshal as in the other
# examples, no difference
```
