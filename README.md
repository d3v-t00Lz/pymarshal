## PyMarshal

pymarshal replicates the feature of (un)marshalling structs in Golang.
Rather than attempting to replicate the exact feature as it exists in Go,
pymarshal aims for elegant, Pythonic simplicity, and to fix the flaws in
Go's implementation such as:
  - extra keys being silently ignored
  - lack of mandatory fields
  - lack of default values

Currently supported formats:
  - JSON
  - BSON

The only modification required to your class code is to use the `type_assert`
functions to assign `__init__` arguments to self variables of the same
name.  pymarshal provides the `type_assert` function to both enforce the type,
and to unmarshal nested objects.  Your `__init__` methods should only use
simple assignment through the `type_assert` functions.  If you have a
use-case for a constructor that does more than simple assignment, use a
separate 'factory' function.

There is also:
  - `type_assert_iter` for iterables
  - `type_assert_dict` for anything that implements .items() -> k, v

Rather than using the Golang "tag" syntax, simply create a
`_marshal_key_swap` and `_unmarshal_key_swap` dict in your class,
and any re-named keys will be swapped before being passed to the
class constructor or before being marshalled to JSON.  The full list
of control variables are documented in `ClassB`
[HERE](https://github.com/j3ffhubb/pymarshal/tree/master/examples/usage_json.md).

## Examples

[Examples](https://github.com/j3ffhubb/pymarshal/tree/master/examples/)

