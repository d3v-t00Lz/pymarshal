"""

"""

import collections

import pytest

from pymarshal.util.checks import *


def test_check_dups():
    # should not raise
    check_dups([1, 2, 3])

def test_check_dups_empty():
    # should not raise
    check_dups([])

def test_check_dups_raises():
    for iterable, debug_limit in (
        ([1, 2, 3, 3], 1000),
        ([1, 2, 2], 1),
    ):
        with pytest.raises(ValueError):
            check_dups(iterable, debug_limit)
