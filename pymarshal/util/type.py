"""

"""

from .marshal import unmarshal_dict
from .key_swap import key_swap


__all__ = [
    'type_assert',
    'type_assert_dict',
    'type_assert_iter',
]


def _check(
    obj,
    cls,
    allow_none=False,
):
    if (
        allow_none
        and
        obj is None
    ):
        return obj

    if not isinstance(obj, cls):
        if isinstance(obj, dict):
            obj = key_swap(obj, cls, True)
            return unmarshal_dict(obj, cls)
        msg = '{0} is not an instance of {1}, is {2}'.format(
            obj,
            cls,
            type(obj),
        )
        raise TypeError(msg)
    return obj


def type_assert(
    obj,
    cls,
    allow_none=False,
):
    """ Wrapper function for isinstance.

        Note that you cannot use this to unmarshal JSON if @cls
        is a tuple of types, it can only be a single type.

        Will also unmarshal JSON objects to Python objects if @obj
        is an instance of dict and @cls is not dict

        Args:
            obj: object instance, The object to type assert
            cls: type, The class type to assert
        Returns:
            @obj
        Raises:
            TypeError: if @obj is not an instance of @cls
    """
    return _check(
        obj,
        cls,
        allow_none,
    )


def type_assert_iter(
    iterable,
    cls,
):
    """ Checks that every object in @iterable is an instance of @cls

        Will also unmarshal JSON objects to Python objects if items in
        @iterable are an instance of dict

        Args:
            iterable:   Any iterable to check.  Note that it would not
                        make sense to pass a generator to this function
            cls:        type, The class type to assert
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
    vcls=None,
    allow_none=False,
):
    """ Checks that every key/value in @d is an instance of @kcls: @vcls

        Will also unmarshal JSON objects to Python objects if
        the value is an instance of dict and @vcls is a class type

        Args:
            d:           The dict to type assert
            @kcls:       The class to type assert for keys.
                         NOTE: JSON only allows str keys
            @vcls:       The class to type assert for values
            @allow_none: Allow a None value for the values.
                         This would not make sense for the keys.
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
            _check(v, vcls, allow_none) if vcls else v,
        )
        for k, v in d.items()
    )

