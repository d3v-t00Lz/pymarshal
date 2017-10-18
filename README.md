## PyMarshal

pymarshal replicates the features of (un)marshalling structs to/from
JSON in Golang.  Rather than attempting to replicate the exact
feature as it exists in Go, pymarshal aims for elegant,
Pythonic simplicity, and to fix the flaws in Go's implementation
such as:
  - extra keys being silently ignored
  - lack of mandatory fields
  - lack of default values

The only modification required to your class code is to use the `type_assert`
functions to assign `__init__` arguments to self variables of the same
name.  pymarshal provides the `type_assert` function to both enforce the type,
and to unmarshal nested objects.

There is also:
  - `type_assert_iter` for iterables
  - `type_assert_dict` for anything that implements .items() -> k, v

Rather than using the Golang "tag" syntax, simply create a
`_marshal_key_swap` and `_unmarshal_key_swap` dict in your class,
and any re-named keys will be swapped before being passed to the
class constructor or before being marshalled to JSON.  The full list
of control variables are documented in `ClassB` below.

## Example

```python
from pymarshal import *

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
    # Optional: Instead of using '_marshal_exclude', you can explicitly
    # exclude all keys that are not part of __init__().
    # Note:
    #     - This will cause _marshal_exclude to be ignored
    #     - The __init__ args must match the class member names

    # _marshal_only_init_args = True

    # Optional: Set to False to forbid extra keys from being present in
    # the JSON object to unmarshal from.  Defaults to True if not present.
    # This overrides allow_extra_keys=True in unmarshal_json, and is
    # the only way to control extra keys from within nested objects

    # _unmarshal_allow_extra_keys = False

    def __init__(self, c):
        self.c = type_assert(c, float)
        # this will be ignored when marshalling because
        # of _marshal_exclude
        self.z = None

>>> j = {"a": 6, "b": {"C": 4.2}}
>>> # pass allow_extra_keys=False to raise an exception when j has
>>> # extra keys not present in ClassA.__init__() arguments
>>> obj1 = unmarshal_json(j, ClassA)
>>> obj1.a
6
>>> obj1.b.c
4.2
>>> obj2 = ClassA(12, ClassB(1.5))
>>> marshal_json(obj2)
{"a": 12, "b": {"C": 1.5}, "b2": None}
```
