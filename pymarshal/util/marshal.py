"""

"""

from .init_args import init_args
from .key_swap import key_swap


__all__ = [
    'ExtraKeysError',
    '_get_dict',
    'InitArgsError',
    'marshal_dict',
    'unmarshal_dict',
]


def _get_dict(obj):
    """ Hack to work around the lack of __dict__ when __slots__ is used

    """
    has_slots = hasattr(obj, '__slots__')
    if has_slots:
        d = {k:getattr(obj, k) for k in obj.__slots__}
    else:
        d = obj.__dict__
    return has_slots, d


class ExtraKeysError(Exception):
    """ Raised when extra object keys are present

        This exception can be marshalled into JSON for sending
        to clients.  However, it cannot be unmarshalled back into
        an ExtraKeysError
    """
    def __init__(
        self,
        cls,
        diff,
    ):
        """ Note that type_assert can't be used because it would
            create a circular dependency.

        Args:
            cls,  type, The type that was attempted to unmarshal into
            diff: dict, The extra arguments that were passed to @cls
        """
        Exception.__init__(self)
        self.type = str(
            type(self),
        )
        self.cls = str(cls)
        self.diff = str(diff)
        self.type = self.__class__.__name__


class InitArgsError(Exception):
    """ Raised when unmarshalling a class raises an Exception

        This exception can be marshalled into JSON for sending
        to clients.  However, it cannot be unmarshalled back into
        an InitArgsError
    """
    def __init__(
        self,
        cls,
        cls_args,
        kwargs,
        ex,
    ):
        """ Note that type_assert can't be used because it would
            create a circular dependency.

        Args:
            cls,      type, The type that was attempted to unmarshal into
            cls_args: list, The arguments of @cls
            kwargs:   dict, The arguments that were passed to @cls
            ex:       Exception, The exception that was raised
        """
        Exception.__init__(self)
        self.type = str(
            type(self),
        )
        self.cls = str(cls)
        self.cls_args = str(cls_args)
        self.kwargs = str(kwargs)
        self.ex = str(ex)
        self.type = self.__class__.__name__


def marshal_dict(
    obj,
    types,
    method=None,
    fields=None,
    **m_kwargs
):
    """ Recursively marshal a Python object to a dict
        that can be passed to json.{dump,dumps}, a web client,
        or a web server, document database, etc...

    Args:
        obj:      object, It's members can be nested Python
                  objects which will be converted to dictionaries
        types:    tuple-of-types, The primitive types that can be
                  serialized
        method:   None-or-str, None to use 'marshal_dict' recursively,
                  or a str that corresponds to the name of a class method
                  to use.  Any nested types that are not an instance of
                  @types must have this method defined.
        fields:   None-list-of-str, Explicitly marshal only these fields
        m_kwargs: Keyword arguments to pass to @method
    Returns:
        dict
    """

    has_slots, d = _get_dict(obj)

    if fields:
        for field in fields:
            assert field in d
        return {
            k: v if isinstance(v, types) else (
                getattr(v, method)(**m_kwargs)
                if method
                else marshal_dict(v, types)
            )
            for k, v in d.items()
            if k in fields
        }

    excl = getattr(obj, '_marshal_exclude', [])

    if (
        has_slots
        or
        getattr(obj, '_marshal_only_init_args', False)
    ):
        args = init_args(obj)
        excl.extend([x for x in d if x not in args])

    if getattr(obj, '_marshal_exclude_none', False):
        excl.extend(k for k, v in d.items() if v is None)
    else:
        none_keys = getattr(obj, '_marshal_exclude_none_keys', [])
        if none_keys:
            excl.extend(x for x in none_keys if d.get(x) is None)

    return {
        k: v if isinstance(v, types) else (
            getattr(v, method)(**m_kwargs)
            if method
            else marshal_dict(v, types)
        )
        for k, v in d.items()
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
        raise ExtraKeysError(cls, diff)

    try:
        return cls(**kwargs)
    except ExtraKeysError as ex:
        raise ex
    except Exception as ex:
        raise InitArgsError(
            cls,
            args,
            kwargs,
            ex,
        )

