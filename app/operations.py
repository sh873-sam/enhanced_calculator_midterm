"""
Arithmetic operations for the enhanced calculator.
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def power(a, b):
    return a ** b


def root(a, b):
    if b == 0:
        raise ValueError("Root degree cannot be zero.")
    return a ** (1 / b)


def modulus(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a % b


def int_divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a // b


def percent(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return (a / b) * 100


def abs_diff(a, b):
    return abs(a - b)