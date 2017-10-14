"""

"""

__all__ = [
    'key_swap',
]


def key_swap(obj, cls):
    if hasattr(cls, '_pm_key_swap'):
        key_swap = cls._pm_key_swap
        return {
            key_swap[k] if k in key_swap else k: v
            for k, v in obj.items()
        }
    else:
        return obj
