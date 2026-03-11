"""
Validates user input for the calculator.
"""


def validate_number(value):
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Invalid number: {value}")


def validate_operation(operation, valid_operations):
    if operation not in valid_operations:
        raise ValueError(f"Invalid operation: {operation}")
    return operation