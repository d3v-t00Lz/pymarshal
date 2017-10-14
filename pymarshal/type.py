"""

"""

from .key_swap import key_swap


__all__ = [
    'type_assert',
    'type_assert_iter',
]


def _check(obj, cls):
    if not isinstance(obj, cls):
        if isinstance(obj, dict):
            obj = key_swap(obj, cls, True)
            return cls(**obj)
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

        Will also unmarshal JSON objects to Python objects if @obj
        is an instance of dict

        Returns:
            @iterable, note that @iterable will be recreated, which
            may be a performance concern if @iterable has many items
        :raises TypeError: if @obj is not an instance of @cls
    """
    t = type(iterable)
    return t(
        _check(obj, cls) for obj in iterable
    )

