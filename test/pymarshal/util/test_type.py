"""

"""

import collections
import os
import pytest

from pymarshal.util.type import *
from pymarshal.util.type import (
    _check,
    _check_choices,
    _check_dstruct,
)


def test_check_dstruct():
    for obj, cls in (
        ([], list),
        (set(), set),
        ({}, dict),
    ):
        _check_dstruct(obj, cls)


def test_check_dstruct_raises():
    for obj, cls in (
        ([], dict),
        ({}, collections.OrderedDict),
        #(collections.OrderedDict(), dict),
    ):
        with pytest.raises(TypeError):
            _check_dstruct(obj, cls)


def test_check_choices():
    for obj, choices in [
        (5, [1, 3, 5]),
        ("a", set(["a", "b", "c"])),
    ]:
        # should not raise
        _check_choices(obj, choices)


def test_check_choices():
    for obj, choices in [
        (4, [1, 3, 5]),
        ("d", set(["a", "b", "c"])),
    ]:
        with pytest.raises(ValueError):
            _check_choices(obj, choices)


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


def test_type_assert_iter_dynamic():
    for dynamic, obj_type in (
        ([5, 6, 7], int),
        ([4.2, 5.7, 9.2], float),
        ([object()], object),
    ):
        # should not raise
        assert dynamic == type_assert_iter(None, obj_type, dynamic=dynamic)


def test_type_assert_iter_choices():
    for obj, obj_type in (
        ([5, 6, 7], int),
        ([4.2, 5.7, 9.2], float),
        ([object()], object),
    ):
        # should not raise
        assert obj == type_assert_iter(obj, obj_type, choices=obj)


def test_type_assert_iter_none():
    assert type_assert_iter(
        None,
        str,
        allow_none=True,
    ) is None


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


def test_type_assert_dict_dynamic():
    for dynamic, kcls, vcls in (
        ({5: "a", 6: "b"}, int, str),
        ({5: "a", 6: "b"}, None, None),
        ({"a": 4.2, "b": 5.7}, str, float),
    ):
        # should not raise or change the value
        assert dynamic == type_assert_dict(None, kcls, vcls, dynamic=dynamic)

def test_type_assert_list():
    class A:
        def __init__(self, a, b):
            self.a = a
            self.b = b
    a = type_assert([1, 2], A)
    assert a.a == 1 and a.b == 2, a.__dict__

def test__check_false_to_none():
    for val, t in (
        (0, int),
        ("", str),
        ([], list),
        ({}, dict),
    ):
        assert _check(val, t, false_to_none=True) is None

def test__check_check_fails():
    for val, t, check in (
        (
            -12,
            int,
            lambda x: x in range(0, 128),
        ),
        (
            "test",
            str,
            lambda x: "lol" in x,
        ),
    ):
        with pytest.raises(ValueError):
            _check(val, t, check=check)

def test__check_from_terminal():
    """ Simulates the OSError from inspect.getsource when run from the
        Python terminal
    """
    def _getsource(*args):
        raise OSError
    import inspect
    getsource = inspect.getsource
    inspect.getsource = _getsource
    try:
        with pytest.raises(ValueError):
            _check({}, dict, check=lambda x: False)
    finally:
        inspect.getsource = getsource

def test_env_var():
    env_var = 'PYMARSHAL_TEST'
    os.environ[env_var] = "y"
    value = type_assert("x", str, env_var=env_var)
    assert value == 'y', value

def test_env_var_cast():
    env_var = 'PYMARSHAL_TEST'
    os.environ[env_var] = "6"
    value = type_assert(
        None,
        int,
        cast_from=str,
        env_var=env_var,
        allow_none=False,
    )
    assert value == 6, value

def test_env_var_none():
    env_var = 'PYMARSHAL_TEST'
    os.environ[env_var] = "y"
    value = type_assert(None, str, env_var=env_var, allow_none=False)
    assert value == 'y', value

