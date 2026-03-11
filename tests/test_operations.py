import pytest

from app.operations import (
    abs_diff,
    add,
    divide,
    int_divide,
    modulus,
    multiply,
    percent,
    power,
    root,
    subtract,
)


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(10, 4) == 6


def test_multiply():
    assert multiply(3, 5) == 15


def test_divide():
    assert divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        divide(10, 0)


def test_power():
    assert power(2, 3) == 8


def test_root():
    assert root(9, 2) == 3


def test_root_degree_zero():
    with pytest.raises(ValueError, match="Root degree cannot be zero."):
        root(9, 0)


def test_modulus():
    assert modulus(10, 3) == 1


def test_modulus_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        modulus(10, 0)


def test_int_divide():
    assert int_divide(10, 3) == 3


def test_int_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        int_divide(10, 0)


def test_percent():
    assert percent(25, 200) == 12.5


def test_percent_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        percent(25, 0)


def test_abs_diff():
    assert abs_diff(3, 10) == 7