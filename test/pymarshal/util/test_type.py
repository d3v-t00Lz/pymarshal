"""

"""

import pytest

from pymarshal.util.type import *


def test_type_assert():
    for obj, obj_type in (
        (5, int),
        (4.2, float),
        (object(), object),
    ):
        # should not raise
        type_assert(obj, obj_type)


def test_type_assert_allow_none():
    for cls in (
        int,
        float,
        object,
    ):
        # should not raise
        assert type_assert(None, cls, allow_none=True) is None


def test_type_assert_raises():
    for obj, cls in (
        (5, float),
        (4.2, int),
    ):
        with pytest.raises(TypeError):
            type_assert(obj, cls)


def test_type_assert_cast_raises():
    for obj, cls, cast_from, cast_to in (
        (5, float, int, str),
    ):
        with pytest.raises(TypeError):
            type_assert(
                obj,
                cls,
                cast_from=cast_from,
                cast_to=cast_to,
            )


def test_type_assert_cast_from():
    for obj, cls, cast_from, cast_to, expected in (
        ("5", int, str, int, 5),
        ("5", int, str, None, 5),
        ("0xff", int, str, lambda x: int(x, 16), 255),
    ):
        assert type_assert(
            obj,
            cls,
            cast_from=cast_from,
            cast_to=cast_to,
        ) == expected


def test_type_assert_dynamic():
    for obj, cls, dynamic, expected in (
        (None, int, 50, 50),
        (None, str, "test", "test"),
        ("test", str, "nope", "test"),
    ):
        assert type_assert(
            obj,
            cls,
            dynamic=dynamic,
        ) == expected


def test_type_assert_dynamic_raises():
    for obj, cls, dynamic, ex in (
        (None, int, "50", TypeError),
        (None, str, 15, TypeError),
    ):
        with pytest.raises(ex):
            type_assert(
                obj,
                cls,
                dynamic=dynamic,
            )


def test_type_assert_iter():
    for obj, obj_type in (
        ([5, 6, 7], int),
        ([4.2, 5.7, 9.2], float),
        ([object()], object),
    ):
        # should not raise
        assert obj == type_assert_iter(obj, obj_type)


def test_type_assert_dict():
    for d, kcls, vcls in (
        ({5: "a", 6: "b"}, int, str),
        ({5: "a", 6: "b"}, None, None),
        ({"a": 4.2, "b": 5.7}, str, float),
    ):
        # should not raise or change the value
        assert d == type_assert_dict(d, kcls, vcls)


def test_type_assert_dict_raises():
    for d, kcls, vcls in (
        ({5: "a", 6: "b"}, str, str),
        ({5: "a", 6: "b"}, None, int),
        ({5: "a", 6: "b"}, str, None),
    ):
        with pytest.raises(TypeError):
            type_assert_dict(d, kcls, vcls)

