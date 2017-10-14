"""

"""

__all__ = [
    'key_swap',
]


def key_swap(
    d,
    cls,
    marshal
):
    """ Swap the keys in a dictionary

        Args:
            d:       dict, The dict to swap keys in
            cls:     class, If the class has a staticly defined
                     _marshal_key_swap and/or _unmarshal_key_swap dict,
                     the keys will be swapped.
                     Otherwise @d is returned
            marshal: bool, True if marshalling class to JSON,
                     False if unmarshalling JSON to class
        Returns:
            dict
    """
    dname = '_{}marshal_key_swap'.format("" if marshal else "un")
    if hasattr(cls, dname):
        key_swap = getattr(cls, dname)
        return {
            key_swap[k] if k in key_swap else k: v
            for k, v in d.items()
        }
    else:
        return d
