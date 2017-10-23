"""

"""

import inspect


def init_args(cls):
    """ Return the __init__ args (minus 'self') for @cls

        Args:
            cls: class or instance
        Returns:
            list of str, the __init__ arguments minus 'self'
        Raises:
            ValueError if __init__ does not have a 'self' argument
    """
    argspec = inspect.getargspec(cls.__init__)
    args = argspec.args
    # raises ValueError if not present.  Not having a self argument
    # in __init__ is almost certainly a user error, and if not
    # there is a special place in hell for people who call the first
    # argument anything but 'self'
    args.remove('self')
    return args

