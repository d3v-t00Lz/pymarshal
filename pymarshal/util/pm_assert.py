from typing import Any, Optional


def pm_assert(
    condition,
    exc: Any=Exception,
    context: Any=None,
    msg: str="",
    ret: Optional[Any]=None,
) -> Optional[Any]:
    """ Generic assertion that can be used anywhere
        @condition: A condition to assert is true
        @exc:       Raise if @condition is False
        @context:   The relevant data structures
        @msg:       Any additional text to include
        @ret:       return value if @condition is True
    """
    if not condition:
        raise exc(f"{msg}\n{context}")
    return ret if ret is not None else condition

