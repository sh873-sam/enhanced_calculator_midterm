"""
Custom exceptions for the calculator application.
"""


class CalculatorError(Exception):
    """Base exception for calculator errors."""


class OperationError(CalculatorError):
    """Raised for invalid operations or math operation issues."""


class ValidationError(CalculatorError):
    """Raised for invalid user input or invalid configuration values."""


class PersistenceError(CalculatorError):
    """Raised for file save/load related issues."""