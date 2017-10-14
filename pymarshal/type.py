"""

"""

from .json import unmarshal_json
from .key_swap import key_swap


__all__ = [
    'type_assert',
    'type_assert_dict',
    'type_assert_iter',
]


def _check(obj, cls):
    if not isinstance(obj, cls):
        if isinstance(obj, dict):
            obj = key_swap(obj, cls, True)
            return unmarshal_json(obj, cls)
        msg = '{0} is not an instance of {1}, is {2}'.format(
            obj,
            cls,
            type(obj),
        )
        raise TypeError(msg)
    return obj


def type_assert(obj, cls):
    """ Wrapper function for isinstance.  See help(isinstance) for args

        Note that you cannot use this to unmarshal JSON if @cls
        is a tuple of types, it can only be a single type.

        Will also unmarshal JSON objects to Python objects if @obj
        is an instance of dict and @cls is not dict

        Returns:
            @obj
        Raises:
            TypeError: if @obj is not an instance of @cls
    """
    return _check(obj, cls)


def type_assert_iter(iterable, cls):
    """ Checks that every object in @iterable is an instance of @cls

        Will also unmarshal JSON objects to Python objects if items in
        @iterable are an instance of dict

        Returns:
            @iterable, note that @iterable will be recreated, which
            may be a performance concern if @iterable has many items
        Raises:
            TypeError: if @obj is not an instance of @cls
    """
    t = type(iterable)
    return t(
        _check(obj, cls) for obj in iterable
    )


def type_assert_dict(
    d,
    kcls=None,
    vcls=None
):
    """ Checks that every key/value in @d is an instance of @kcls/@vcls

        Will also unmarshal JSON objects to Python objects if
        the value is an instance of dict and @vcls is a class type

        Returns:
            @d, note that @d will be recreated, which
            may be a performance concern if @d has many items
        Raises:
            TypeError: if a key is not an instance of @kcls or
                       a value is not an instance of @vcls
    """
    t = type(d)
    return t(
        (
            _check(k, kcls) if kcls else k,
            _check(v, vcls) if vcls else v,
        )
        for k, v in d.items()
    )

