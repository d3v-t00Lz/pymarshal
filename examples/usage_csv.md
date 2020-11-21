```python
>>> from pymarshal.csv import *
>>> class Test:
...   def __init__(
...     self,
...     a,
...     b,
...   ):
...     self.a = type_assert(a, int, cast_from=str)
...     self.b = type_assert(b, str, cast_from=str)
...
>>> u = [Test(1, "a"), Test(3, "b")]
>>> m = marshal_csv(u, Test)
>>> m
[[1, 'a'], [3, 'b']]
>>> u2 = unmarshal_csv(m, Test)
>>> u2
[
  <__main__.Test object at 0x7fa1eb127b80>,
  <__main__.Test object at 0x7fa1eb127f10>,
]
>>> with open('/tmp/test-pymarshal.csv', 'w') as f:
...   w = csv.writer(f)
...   w.writerows(m)
...

>>> with open('/tmp/test-pymarshal.csv') as f:
...   r = csv.reader(f)
...   u3 = unmarshal_csv(list(r), Test)
...
>>> u3
[
  <__main__.Test object at 0x7fa1eaf5cfa0>,
  <__main__.Test object at 0x7fa1eaf5ca00>,
]

```
