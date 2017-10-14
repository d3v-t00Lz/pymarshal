"""

"""

import pytest

from pymarshal.type import *


def test_type_assert():
    for obj, obj_type in (
        (5, int),
        (4.2, float),
        (object(), object),
    ):
        # should not raise
        type_assert(obj, obj_type)


def test_type_assert_raises():
    for obj, obj_type in (
        (5, float),
        (4.2, int),
    ):
        with pytest.raises(TypeError):
            type_assert(obj, obj_type)


def test_type_assert_iter():
    for obj, obj_type in (
        ([5, 6, 7], int),
        ([4.2, 5.7, 9.2], float),
        ([object()], object),
    ):
        # should not raise
        type_assert_iter(obj, obj_type)


