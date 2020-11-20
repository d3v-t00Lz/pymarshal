```python
# YAML is compatible with JSON, so use the
# JSON module with YAML-formatted data
from pymarshal.json import *
# Be sure to 'pip install PyYAML' first
import yaml

class Y:
   def __init__(self, a, b):
     self.a = type_assert(a, int)
     self.b = type_assert_iter(b, int)

>>> # Convert an instance of Y to a YAML str
>>> y = Y(1, [2, 3, 4])
>>> m = marshal_json(y)
>>> m
{'a': 1, 'b': [2, 3, 4]}
>>> yml_str = yaml.dump(m)
>>> print(yml_str)
a: 1
b: [2, 3, 4]
>>> # Create a new Y instance from yml_str
>>> yml_obj = yaml.safe_load(yml_str)
>>> y2 = unmarshal_json(yml_obj, Y)
```
