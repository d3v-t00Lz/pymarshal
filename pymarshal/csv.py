"""

"""

from .util.marshal import *
from .util.type import *


__all__ = [
    'InitArgsError',
    'marshal_csv',
    'type_assert',
    'type_assert_iter',
    'unmarshal_csv',
]

CSV_TYPES = (
    float,
    int,
    str,
)

def marshal_csv(
    iterable,
    cls,
    types=CSV_TYPES,
    fields=None,
):
    """ Marshal a list of Python objects to a CSV-compatible list of lists
        that can be passed to csv.writer.writerows

    Args:
        iterable: list, A list of objects that do not contain nested objects,
                  all fields must be of types in @types
        cls:      type-or-function,
        types:    tuple-of-types, The primitive types, typically
                  you would not change this
        fields:   None-or-list-of-str, Explicitly marshal only these fields
    Returns:
        dict
    """
    return [
        marshal_list(
            x,
            cls,
            types,
            fields,
        ) for x in iterable
    ]


def unmarshal_csv(
    iterable,
    cls,
):
    """ Unmarshal @iterable into a list of @cls

    Args:
        iterable: list-or-tuple-of-objects
        cls:      type-or-function, The type to unmarshal into
    Returns:
        List of instances of @cls
    Raises:
        ValueError: If @cls.__init__ does not contain a self argument
    """
    return [
        unmarshal_list(x, cls)
        for x in iterable
    ]
