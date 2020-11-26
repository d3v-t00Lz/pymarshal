from pymarshal import pm_assert
import pytest


ARGS = (
    (Exception, {"a": 1}, "test"),
    (OSError, None, "test3"),
    (KeyError, 3, "test4"),
    (ValueError, None, "test5"),
    (IndexError, [], "test6"),
)

def test_pm_assert():
    for exc, context, msg in ARGS:
        pm_assert(True, exc, context, msg)

def test_pm_assert_raises():
    for exc, context, msg in ARGS:
        with pytest.raises(exc):
            pm_assert(False, exc, context, msg)

