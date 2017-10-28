```python
class ControlVars:
    # Optional: Replaces keys in the JSON object before
    # passing to __init__()
    # Useful for JSON keys that are not valid Python variable names
    _unmarshal_key_swap = {
        "C": "c",
    }
    # Optional: Controls mapping the keys back to JSON.
    # If unmarshalling doesn't map multiple keys to the same value,
    # you can simply use:
    # {v: k for k, v in _unmarshal_key_swap.items()}
    _marshal_key_swap = {
        "c": "C",
    }
    # Optional: Ignores these members when marshalling to JSON
    _marshal_exclude = [
        'z',
    ]
    # Optional: Instead of using '_marshal_exclude', you can explicitly
    # exclude all keys that are not part of __init__().
    # Note:
    #     - This will cause _marshal_exclude to be ignored
    #     - The __init__ args must match the class member names

    # _marshal_only_init_args = True

    # Optional: Set to False to forbid extra keys from being present in
    # the JSON object to unmarshal from.  Defaults to True if not present.
    # This overrides allow_extra_keys=True in unmarshal_json, and is
    # the only way to control extra keys from within nested objects

    # _unmarshal_allow_extra_keys = False

    # Optional: Exclude any key whose value is None when marshalling
    # The __init__ args this may affect should have a default value of None
    # and type_assert(..., allow_none=True) in the assignment

    _marshal_exclude_none = True

    # Optional: Exclude specific keys if their value is None when marshalling
    # The corresponding __init__ args should have a default value of None
    # and type_assert(..., allow_none=True) in the assignment
    # There is no need to set this if _marshal_exclude_none == True

    # _marshal_exclude_none_keys = ['key1', 'key2']

    def __init__(self, c, z="test", none=None):
        self.c = type_assert(c, float)
        # this will be ignored when marshalling because
        # of _marshal_exclude
        self.z = type_assert(z, str)
        # this will be ignored when marshalling because
        # of _marshal_exclude_none==True, assuming the
        # default value of None is used
        self.none = type_assert(none, str, allow_none=True)
```
