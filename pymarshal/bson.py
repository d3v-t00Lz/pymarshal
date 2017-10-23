"""

"""

# Will raise an import error if the user hasn't installed 'bson'
import bson
import datetime

from .util.marshal import *
from .util.type import *


__all__ = [
    'ExtraKeysError',
    'marshal_bson',
    'MongoDocument',
    'type_assert',
    'type_assert_dict',
    'type_assert_iter',
    'unmarshal_bson',
]


BSON_TYPES = (
    bool,
    bson.ObjectId,
    datetime.datetime,
    dict,
    float,
    int,
    list,
    str,
    type(None),
)


class MongoDocument:
    """ Abstract class to facilitate inserting into MongoDB.
        Inherit this for classes that represent BSON documents.

        Assumes that you assigned the ObjectId in your
        class like:

            def __init__(
                self,
                ...,
                _id=None,
                ...,
            ):

            self._id = type_assert(
                _id,
                bson.ObjectId,
                allow_none=True,
            )
    """
    _marshal_exclude_none_keys = ['_id']


def marshal_bson(
    obj,
    types=BSON_TYPES,
):
    """ Recursively marshal a Python object to a BSON-compatible dict
        that can be passed to PyMongo, Motor, etc...

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
