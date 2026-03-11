"""
Represents a single calculator calculation.
"""

from app.operations import (
    add,
    subtract,
    multiply,
    divide,
    power,
    root,
    modulus,
    int_divide,
    percent,
    abs_diff
)


class Calculation:
    def __init__(self, operation, a, b):
        self.operation = operation
        self.a = a
        self.b = b

    def perform(self):
        operations = {
            "add": add,
            "subtract": subtract,
            "multiply": multiply,
            "divide": divide,
            "power": power,
            "root": root,
            "modulus": modulus,
            "int_divide": int_divide,
            "percent": percent,
            "abs_diff": abs_diff,
        }

        if self.operation not in operations:
            raise ValueError(f"Invalid operation: {self.operation}")

        return operations[self.operation](self.a, self.b)