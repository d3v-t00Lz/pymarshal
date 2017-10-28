```python
from pymarshal.json import *

class ClassA:
    def __init__(self, a, b, b2=None):
        self.a = type_assert(a, int)
        # If 'b' is an instance of ClassB, it will simply pass through
        # If 'b' is a dictionary, it will be unmarshalled into a new
        #     ClassB instance using ClassB(**b)
        # If neither, it will raise TypeError
        self.b = type_assert(b, ClassB)
        # Use allow_none=True to allow this value to be None instead of
        # an instance of ClassB
        self.b2 = type_assert(b2, ClassB, allow_none=True)

class ClassB:
    # Optional: Replaces keys in the JSON object before
    # passing to __init__()
    # Useful for JSON keys that are not valid Python variable names
    _unmarshal_key_swap = {
        "C": "c",
    }
    # Optional: Controls mapping the keys back to JSON.
    # If unmarshalling doesn't map multiple keys to the same value,
    # you can simply use:
    # {v: k for k, v in _unmarshal_key_swap.items()}
    _marshal_key_swap = {
        "c": "C",
    }
    # Optional: Ignores these members when marshalling to JSON
    _marshal_exclude = [
        'z',
    ]

    def __init__(self, c):
        self.c = type_assert(c, float)
        # this will be ignored when marshalling because
        # of _marshal_exclude
        self.z = "test"

>>> # Unmarshal JSON data to an instance of ClassA
>>> j = {"a": 6, "b": {"C": 4.2}}
>>> # pass allow_extra_keys=False to raise an exception when j has
>>> # extra keys not present in ClassA.__init__() arguments
>>> obj1 = unmarshal_json(j, ClassA)
>>> obj1.a
6
>>> obj1.b.c
4.2
>>> # Marshal an instance of ClassA to JSON-compatible data structures
>>> obj2 = ClassA(12, ClassB(1.5))
>>> marshal_json(obj2)
{"a": 12, "b": {"C": 1.5}, "b2": None}
```
