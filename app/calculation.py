"""
Represents a single calculator calculation using a simple factory pattern.
"""

from app.exceptions import OperationError
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


class Calculation:
    operation_map = {
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

    def __init__(self, operation, a, b):
        self.operation = operation
        self.a = a
        self.b = b

    @classmethod
    def create(cls, operation, a, b):
        if operation not in cls.operation_map:
            raise OperationError(f"Invalid operation: {operation}")
        return cls(operation, a, b)

    def perform(self):
        if self.operation not in self.operation_map:
            raise OperationError(f"Invalid operation: {self.operation}")

        try:
            result = self.operation_map[self.operation](self.a, self.b)
            return round(result, self._precision())
        except ZeroDivisionError as exc:
            raise OperationError("Cannot divide by zero.") from exc
        except ValueError as exc:
            raise OperationError(str(exc)) from exc

    @staticmethod
    def _precision():
        from app.calculator_config import Config

        return Config.CALCULATOR_PRECISION