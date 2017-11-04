"""

"""

import inspect
import sys
import types


def init_args(cls):
    """ Return the __init__ args (minus 'self') for @cls

        Args:
            cls: class, instance or callable
        Returns:
            list of str, the __init__ arguments minus 'self'
        Raises:
            ValueError if __init__ does not have a 'self' argument
    """
    # This looks insanely goofy, but seems to literally be the
    # only thing that actually works.  Your obvious ways to
    # accomplish this task do not apply here.
    try:
        # Assume it's a factory function, static method, or other callable
        argspec = inspect.getargspec(cls)
        args = argspec.args
    except TypeError:
        # assume it's a class
        argspec = inspect.getargspec(cls.__init__)
        args = argspec.args

    # Note:  There is a special place in hell for people who don't
    #        call the first method argument 'self'.
    if args[0] == 'self':
        args.remove('self')

    return args

