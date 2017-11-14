"""

"""

from .util.marshal import *
from .util.type import *


__all__ = [
    'ExtraKeysError',
    'InitArgsError',
    'marshal_json',
    'type_assert',
    'type_assert_dict',
    'type_assert_iter',
    'unmarshal_json',
]

JSON_TYPES = (
    bool,
    dict,
    float,
    int,
    list,
    str,
    type(None),
)


def marshal_json(
    obj,
    types=JSON_TYPES,
):
    """ Recursively marshal a Python object to a JSON-compatible dict
        that can be passed to json.{dump,dumps}, a web client,
        or a web server, etc...

        Args:
            obj:   object, It's members can be nested Python
                   objects which will be converted to dictionaries
            types: tuple-of-types, The JSON primitive types, typically
                   you would not change this
        Returns:
            dict
    """
    return marshal_dict(obj, types)


def unmarshal_json(
    obj,
    cls,
    allow_extra_keys=True,
):
    """ Unmarshal @obj into @cls

        Args:
            obj:              dict, A JSON object
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
