.. code-block:: python
   # pymarshal replicates the features of (un)marshalling structs to/from
   # JSON in Golang.
   # pymarshal uses the 'type_assert' function to both enforce the type,
   # and to unmarshal nested objects.  There is also a 'type_assert_iter'
   # function to assure that all items in an iterable

   # Rather than using the Golang "tag" syntax, simply create a
   # '_marshal_key_swap' and '_unmarshal_key_swap' dict in your class,
   # and any re-named keys will be swapped before being passed to the
   # class constructor or before

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
       _unmarshal_key_swap = {
           "C": "c",
       }
       #
       _marshal_key_swap = {
           "c": "C",
       }
       def __init__(self, c):
           self.c = type_assert(c, float)

   >>> j = {"a": 6, "b": {"C": 4.2}}
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

