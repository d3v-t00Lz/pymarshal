"""

"""

import json

from .key_swap import key_swap


__all__ = [
    'marshal_json',
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


def marshal_json(obj):
    """ Recursively marshal a Python object to JSON

        Args:
            obj: A Python object.  It's members can be nested Python
                 objects which will be converted to dictionaries
        Returns:
            dict
    """
    excl = obj._marshal_exclude if hasattr(obj, '_marshal_exclude') else []
    return {
        k: v if isinstance(v, JSON_TYPES) else marshal_json(v)
        for k, v in obj.__dict__.items()
        if k not in excl
    }


def unmarshal_json(obj, cls):
    """ Unmarshal @obj into @cls

        Args:
            obj: dict, A JSON object
            cls: type, The class to unmarshal into
        Returns:
            instance of @cls
    """
    obj = key_swap(obj, cls, False)
    return cls(**obj)

