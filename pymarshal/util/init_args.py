"""

"""

import sys
import types


if sys.version_info >= (3,):  # pragma: no cover
    from inspect import getfullargspec as getargspec
else:  # pragma: no cover
    from inspect import getargspec


def init_args(cls):
    """ Return the __init__ args (minus 'self') for @cls

    Args:
        cls: class, instance or callable
    Returns:
        list of str, the arguments minus 'self'
    """
    # This looks insanely goofy, but seems to literally be the
    # only thing that actually works.  Your obvious ways to
    # accomplish this task do not apply here.
    try:
        # Assume it's a factory function, static method, or other callable
        argspec = getargspec(cls)
    except TypeError:
        # assume it's a class
        argspec = getargspec(cls.__init__)
    args = argspec.args

    # Note:  There is a special place in hell for people who don't
    #        call the first method argument 'self'.
    if args[0] == 'self':
        args.remove('self')

    return args

