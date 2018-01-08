## API Docs

PyMarshal features an integrated API documentation system that uses YAML
or JSON based docstrings:

```python
class MyModel:
    def __init__(
        self,
        a,
        b=5,
    ):
        """
        desc: >
            An example model
            Blah blah, blah blah
        args:
            -   name: a
                type: str
                desc: The a thing
            -   name: b
                type: str
                desc: The b thing
                required: false
                default: 5
        """
        self.a = type_assert(a, str)
        self.b = type_assert(b, int)
```

For a full example of the documentation system in action, see
[THIS](https://github.com/j3ffhubb/mpwdga/tree/master/mpwdga/routes).

For an example of how to convert a Routes instance to routes in your web
framework (Sanic in this case), see
[THIS](https://github.com/j3ffhubb/mpwdga/blob/master/mpwdga/routes/__init__.py).

For an example of how to convert the API docs response object into HTML
using AJAX, see
[THIS](https://github.com/j3ffhubb/mpwdga/blob/master/static-site/src/docs.html).

