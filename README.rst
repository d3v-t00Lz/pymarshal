.. code-block:: python
   # pymarshal replicates the features of (un)marshalling structs to/from
   # JSON in Golang.  Rather than attempting to replicate the exact
   # feature as it exists in Go, pymarshal aims for elegant,
   # Pythonic simplicity, and to fix the flaws in Go's implementation
   # such as:
   #   - extra keys being silently ignored
   #   - lack of mandatory fields

   # pymarshal uses the 'type_assert' function to both enforce the type,
   # and to unmarshal nested objects.  There is also:
   #   - 'type_assert_iter' for iterables
   #   - 'type_assert_dict' for anything that implements .items() -> k, v

   # Rather than using the Golang "tag" syntax, simply create a
   # '_marshal_key_swap' and '_unmarshal_key_swap' dict in your class,
   # and any re-named keys will be swapped before being passed to the
   # class constructor or before being marshalled to JSON

   from pymarshal import *

   class ClassA:
       def __init__(self, a, b):
           self.a = type_assert(a, int)
           # If 'b' is an instance of ClassB, it will simply pass through
           # If 'b' is a dictionary, it will be unmarshalled into a new
           #     ClassB instance
           # If neither, it will raise TypeError
           self.b = type_assert(b, ClassB)

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
           self.z = None

   >>> j = {"a": 6, "b": {"C": 4.2}}
   >>> # pass allow_extra_keys=False to raise an exception when j has
   >>> # extra keys not present in ClassA.__init__() arguments
   >>> obj1 = unmarshal_json(j, ClassA)
   >>> type(obj1)
   <class '__main__.ClassA'>
   >>> obj1.a
   6
   >>> ob1.b.c
   4.2
   >>> obj2 = ClassA(12, ClassB(1.5))
   >>> marshal_json(obj2)
   {"a": 12, "b": {"C": 1.5}}

