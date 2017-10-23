"""

"""

# Will raise an import error if the user hasn't installed 'bson'
import bson

from .init_args import init_args
from .key_swap import key_swap
from .marshal import *
from .type import *


__all__ = [
    'ExtraKeysError',
    'marshal_bson',
    'type_assert',
    'type_assert_dict',
    'type_assert_iter',
    'unmarshal_bson',
]

BSON_TYPES = (
    bool,
    bson.ObjectId,
    dict,
    float,
    int,
    list,
    str,
    type(None),
)


def marshal_bson(
    obj,
    types=BSON_TYPES,
):
    """ Recursively marshal a Python object to a BSON-compatible dict
        that can be passed to json.{dump,dumps}, a web client,
        or a web server, etc...

        Args:
            obj:   object, It's members can be nested Python
                   objects which will be converted to dictionaries
            types: tuple-of-types, The BSON primitive types, typically
                   you would not change this
        Returns:
            dict
    """
    return marshal_dict(obj, types)


def unmarshal_bson(
    obj,
    cls,
    allow_extra_keys=True,
):
    """ Unmarshal @obj into @cls

        Args:
            obj:              dict, A BSON object
            cls:              type, The class to unmarshal into
            allow_extra_keys: bool, False to raise an exception when extra
                              keys are present, True to ignore
        Returns:
            instance of @cls
        Raises:
            ExtraKeysError: If allow_extra_keys == False, and extra keys
                            are present in @obj and not in @cls.__init__
            ValueError:     If @cls.__init__ does not contain a self argument
    """
    return unmarshal_dict(
        obj,
        cls,
        allow_extra_keys,
    )
