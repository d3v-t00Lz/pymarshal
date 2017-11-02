```python
# Examples of how to use cast_from and cast_to to dynamically
# cast types.  This is useful when converting incompatible
# types from JSON to BSON, for example.


class A:
    def __init__(
        self,
        a,
    ):
        self.a = type_assert(
            a,
            int,
            cast_from=str,
            # Casts a base-16 str to int
            cast_to=lambda x: int(x, 16),
        )

>>> a = A('0xff')
>>> a.a
255

class B:
    def __init__(
        self,
        b,
    ):
        self.b = type_assert(
            b,
            str,
            cast_from=int,
            #omitting cast_to will cast it to @cls
        )

>>> b = B(5)
>>> b.b
"5"

```

