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

        :returns: dict
    """
    return {
        k: v if isinstance(v, JSON_TYPES) else marshal_json(v)
        for k, v in obj.__dict__.items()
    }


def unmarshal_json(obj, cls):
    """ Unmarshal @obj into @cls

        :param obj:  A JSON object
        :type obj: dict
        :param cls: The class to unmarshal into
        :type cls: class
        :returns: instance of @cls
    """
    obj = key_swap(obj, cls, False)
    return cls(**obj)

