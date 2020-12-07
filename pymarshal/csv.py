"""

"""

from .util.marshal import *
from .util.pm_assert import pm_assert
from .util.type import *


__all__ = [
    'InitArgsError',
    'marshal_csv',
    'pm_assert',
    'type_assert',
    'type_assert_iter',
    'unmarshal_csv',
    'unmarshal_csv_list',
]

CSV_TYPES = (
    float,
    int,
    str,
)

def marshal_csv(
    iterable,
    types=CSV_TYPES,
    fields=None,
):
    """ Marshal a list of Python objects to a CSV-compatible list of lists
        that can be passed to csv.writer.writerows.
        If @iterable is a class instance, it must offer a method to iterate
        through it's objects, or implement __iter__.

    Args:
        iterable: list, A list of objects that do not contain nested objects,
                  all fields must be of types in @types
        types:    tuple-of-types, The primitive types, typically
                  you would not change this
        fields:   None-or-list-of-str, Explicitly marshal only these fields
    Returns:
        dict
    """
    return [
        marshal_list(
            x,
            types,
            fields,
        ) for x in iterable
    ]

def unmarshal_csv(
    iterable,
    cls,
    ignore_extras=False,
):
    """ Unmarshal @iterable into a single instance of @cls
    Args:
        @iterable: list-or-tuple-of-lists
        @cls:
            A class that contains the
            _unmarshal_csv_map = {
                'row_header': {
                    'arg_name': '__init__ arg name',
                    'type': Class,  # Or a factory function
                }
            }
            field to map row headers to input arguments

            Optional:
            _unmarshal_csv_default_arg = {
                'arg_name': '__init__ arg name',
                'type': Class,  # Or a factory function
            }
            to set a default when no recognized header is in the row.
            This type should not implement _marshal_list_row_header

            Optional:
            _unmarshal_csv_singletons = {
                'row_header': {
                    'arg_name': '__init__ arg name',
                    'type': Class,  # Or a factory function
                }
            }
        @ignore_extras:
            bool, True to ignore unrecognized rows, otherwise ValueError is
            raised when an unrecognized row it encountered
    """
    if hasattr(cls, '_unmarshal_csv_map'):
        csv_map = cls._unmarshal_csv_map
    else:
        csv_map = {}
    if hasattr(cls, '_unmarshal_csv_singletons'):
        singletons = cls._unmarshal_csv_singletons
    else:
        singletons = {}
    kwargs = {
        v['arg_name']: []
        for v in cls._unmarshal_csv_map.values()
    }
    if hasattr(cls, '_unmarshal_csv_default_arg'):
        default_arg = cls._unmarshal_csv_default_arg
        default_arg_name = default_arg['arg_name']
        default_arg_type = default_arg['type']
        kwargs[default_arg_name] = []
    else:
        default_arg = None
    pm_assert(
        kwargs or singletons,
        AttributeError,
        msg="""\
            @cls must have one or more of _marshal_csv_map,
            _unmarshal_csv_singletons, _unmarshal_csv_default_arg
        """,
    )
    for x in iterable:
        row_header = x[0]
        if row_header in csv_map:
            arg_name = csv_map[row_header]['arg_name']
            _type = csv_map[row_header]['type']
            value = _type(*x[1:])
            kwargs[arg_name].append(value)
        elif row_header in singletons:
            arg_name = singletons[row_header]['arg_name']
            _type =  singletons[row_header]['type']
            kwargs[arg_name] = _type(*x[1:])
        elif default_arg:
            value = default_arg_type(*x)
            kwargs[default_arg_name].append(value)
        elif not ignore_extras:
            msg = "Unrecognized row: '{}'".format(x)
            raise ValueError(msg)

    return cls(**kwargs)

def unmarshal_csv_list(
    iterable,
    cls,
):
    """ Unmarshal @iterable into a list of @cls
        Assumes that @iterable are all a single type

    Args:
        iterable: list-or-tuple-of-lists
        cls:
            type-or-function or {"row header": function},
            The type to unmarshal into
    Returns:
        List of instances of @cls
    Raises:
        ValueError: If @cls.__init__ does not contain a self argument
    """
    return [
        unmarshal_list(x, cls)
        for x in iterable
    ]

