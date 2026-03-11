import pytest

from app.calculation import Calculation


def test_calculation_perform_add():
    calc = Calculation("add", 2, 3)
    assert calc.perform() == 5


def test_calculation_perform_subtract():
    calc = Calculation("subtract", 10, 4)
    assert calc.perform() == 6


def test_calculation_perform_multiply():
    calc = Calculation("multiply", 3, 5)
    assert calc.perform() == 15


def test_calculation_perform_divide():
    calc = Calculation("divide", 10, 2)
    assert calc.perform() == 5


def test_calculation_invalid_operation():
    calc = Calculation("unknown", 1, 2)
    with pytest.raises(ValueError, match="Invalid operation: unknown"):
        calc.perform()