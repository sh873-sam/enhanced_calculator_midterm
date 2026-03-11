"""
Validates user input for the calculator.
"""

from app.calculator_config import Config
from app.exceptions import ValidationError


def validate_number(value):
    try:
        number = float(value)
    except ValueError as exc:
        raise ValidationError(f"Invalid number: {value}") from exc

    if abs(number) > Config.CALCULATOR_MAX_INPUT_VALUE:
        raise ValidationError(
            f"Input exceeds maximum allowed value: {Config.CALCULATOR_MAX_INPUT_VALUE}"
        )

    return number


def validate_operation(operation, valid_operations):
    if operation not in valid_operations:
        raise ValidationError(f"Invalid operation: {operation}")
    return operation