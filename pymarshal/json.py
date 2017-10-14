"""

"""

import inspect
import json

from .key_swap import key_swap


__all__ = [
    'ExtraKeysError',
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


class ExtraKeysError(Exception):
    """ Raised when extra JSON object keys are present """


def marshal_json(obj):
    """ Recursively marshal a Python object to a JSON-compatible dict
        that can be passed to json.{dump,dumps}, a web client,
        or a web server, etc...

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


def unmarshal_json(obj, cls, allow_extra_keys=True):
    """ Unmarshal @obj into @cls

        Args:
            obj:              dict, A JSON object
            cls:              type, The class to unmarshal into
            allow_extra_keys: bool, False to raise an exception when extra
                              keys are present, True to ignore
        Returns:
            instance of @cls
        Raises:
            ValueError:  If @cls.__init__ does not contain a self argument
    """
    argspec = inspect.getargspec(cls.__init__)
    args = argspec.args
    # raises ValueError if not present.  Not having a self argument
    # in __init__ is almost certainly a user error, and if not
    # there is a special place in hell for people who call the first
    # argument anything but 'self'
    args.remove('self')
    obj = key_swap(obj, cls, False)
    kwargs = {k: v for k, v in obj.items() if k in args}
    if not allow_extra_keys and len(obj) > len(kwargs):
        diff = {k: v for k, v in obj.items() if k not in args}
        msg = "Extra keys present, but allow_extra_keys=={}: {}".format(
            allow_extra_keys,
            diff,
        )
        raise ExtraKeysError(msg)

    return cls(**kwargs)

