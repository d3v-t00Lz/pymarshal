"""

"""

from .init_args import init_args
from .key_swap import key_swap


__all__ = [
    'ExtraKeysError',
    'marshal_dict',
    'unmarshal_dict',
]


class ExtraKeysError(Exception):
    """ Raised when extra object keys are present """


def marshal_dict(
    obj,
    types,
):
    """ Recursively marshal a Python object to a JSON-compatible dict
        that can be passed to json.{dump,dumps}, a web client,
        or a web server, etc...

        Args:
            obj:   object, It's members can be nested Python
                   objects which will be converted to dictionaries
            types: tuple-of-types, The primitive types that can be
                   serialized
        Returns:
            dict
    """
    if getattr(obj, '_marshal_only_init_args', False):
        args = init_args(obj)
        excl = [x for x in obj.__dict__ if x not in args]
    else:
        excl = getattr(obj, '_marshal_exclude', [])

    if getattr(obj, '_marshal_exclude_none', False):
        excl.extend(k for k, v in obj.__dict__.items() if v is None)
    else:
        none_keys = getattr(obj, '_marshal_exclude_none_keys', [])
        if none_keys:
            excl.extend(x for x in none_keys if obj.__dict__.get(x) is None)

    return {
        k: v if isinstance(v, types) else marshal_dict(v, types)
        for k, v in obj.__dict__.items()
        if k not in excl
    }


def unmarshal_dict(
    obj,
    cls,
    allow_extra_keys=True,
):
    """ Unmarshal @obj into @cls

        Args:
            obj:              dict, The dict to unmarshal into @cls
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
    args = init_args(cls)
    obj = key_swap(obj, cls, False)
    kwargs = {k: v for k, v in obj.items() if k in args}

    # If either is set to False, do not allow extra keys
    # to be present in obj but not in cls.__init__
    allow_extra_keys = (
        getattr(cls, '_unmarshal_allow_extra_keys', True)
        and
        allow_extra_keys
    )

    if not allow_extra_keys and len(obj) > len(kwargs):
        diff = {k: v for k, v in obj.items() if k not in args}
        msg = "Extra keys present, but allow_extra_keys=={}: {}".format(
            allow_extra_keys,
            diff,
        )
        raise ExtraKeysError(msg)

    return cls(**kwargs)

