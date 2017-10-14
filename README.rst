.. code-block:: python
   # pymarshal replicates the features of (un)marshalling structs to/from
   # JSON in Golang.
   # pymarshal uses the 'type_assert' function to both enforce the type,
   # and to unmarshal nested objects.

   # Rather than using the Golang "tag" syntax, simply create a
   # '_pm_key_swap' dict in your class, and any re-named keys
   # (or keys that would be invalid Python names)
   # will be swapped before being passed to the class constructor.

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
       # Replaces keys in the JSON object before passing
       # to __init__()
       _pm_key_swap = {
           "C": "c",
       }
       def __init__(self, c):
           self.c = type_assert(c, float)

   >>> j = {"a": 6, "b": {"C": 4.2}}
   >>> obj = unmarshal_json(j, ClassA) # Populate a ClassA object from j
   >>> marshal_json(obj) # convert obj back to j

