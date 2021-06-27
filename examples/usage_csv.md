# CSV

Also see [control variables](
  https://github.com/stargateaudio/pymarshal/blob/master/examples/control_variables.md
) for CSV-related options to marshal and unmarshal complex types
to/from a single CSV list.

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
>>> # Complex CSV types
>>> class CSVRow:
...   _marshal_list_row_header = "c"
...   def __init__(self, a, b):
...     self.a = type_assert(a, int, cast_from=str)
...     self.b = type_assert(b, str)
...
>>> class CSVRow2:
...   _marshal_list_row_header = "c2"
...   def __init__(self, a, b):
...     self.a = type_assert(a, float, cast_from=str)
...     self.b = type_assert(b, str)
...
>>> class ComplexCSV:
...   _unmarshal_csv_map = {
...     "c": {"arg_name": "a", "type": CSVRow},
...     "c2": {"arg_name": "b", "type": CSVRow2},
...   }
...   def __init__(self, a, b):
...     self.a = type_assert_iter(a, CSVRow)
...     self.b = type_assert_iter(b, CSVRow2)
...   def __iter__(self):
...     for x in self.a:
...       yield x
...     for x in self.b:
...       yield x
...
>>> complex = ComplexCSV(
...   [CSVRow(3, "py"), CSVRow(6, "marshal")],
...   [CSVRow2(3.3, "py"), CSVRow2(6.6, "marshal")],
... )
>>> m = marshal_csv(complex)
>>> m
[['c', 3, 'py'], ['c', 6, 'marshal'], ['c2', 3.3, 'py'], ['c2', 6.6, 'marshal']]
>>> u = unmarshal_csv(m, ComplexCSV)
>>> u
<__main__.ComplexCSV object at 0x7f2c8985c730>
>>> u.__dict__
{
  'a': [
    <__main__.CSVRow object at 0x7f2c8985c700>,
    <__main__.CSVRow object at 0x7f2c89858280>,
  ],
  'b': [
    <__main__.CSVRow2 object at 0x7f2c898581f0>,
    <__main__.CSVRow2 object at 0x7f2c89856a00>,
  ],
}
```
