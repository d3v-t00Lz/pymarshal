def pm_assert(
    condition,
    exc=Exception,
    context=None,
    msg="",
):
    """ Generic assertion that can be used anywhere
        @condition: bool, A condition to assert is true
        @exc:       Exception type, Raise if @condition is False
        @context:   Any, The relevant data structures
        @msg:       str, Any additional text to include
    """
    if not condition:
        raise exc(msg + "\n" + str(context))

