"""
    Replicates the functionality of Golang's
    struct (un)marshalling feature to/from JSON.

    For examples, see:
    https://github.com/j3ffhubb/pymarshal/blob/master/README.rst
"""

__version__ = '1.1.2'

__all__ = [
    'ExtraKeysError',
    'marshal_json',
    'type_assert',
    'type_assert_dict',
    'type_assert_iter',
    'unmarshal_json',
]


from .json import *
from .type import *
