"""

"""

__all__ = [
    'key_swap',
]


def key_swap(
    obj,
    cls,
    marshal
):
    """ Swap the keys in a dictionary

        :returns: dict
    """
    dname = '_{}marshal_key_swap'.format("" if marshal else "un")
    if hasattr(cls, dname):
        key_swap = getattr(cls, dname)
        return {
            key_swap[k] if k in key_swap else k: v
            for k, v in obj.items()
        }
    else:
        return obj
