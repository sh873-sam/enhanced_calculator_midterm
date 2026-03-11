"""
Manages calculation history and persistence.
"""

from datetime import datetime
from pathlib import Path

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import Config
from app.exceptions import PersistenceError


class History:
    def __init__(self):
        self.history = []

    def add(self, calculation):
        calculation.timestamp = datetime.now()

        self.history.append(calculation)

        if len(self.history) > Config.CALCULATOR_MAX_HISTORY_SIZE:
            self.history.pop(0)

    def get_all(self):
        return self.history

    def clear(self):
        self.history.clear()

    def last(self):
        if not self.history:
            return None
        return self.history[-1]

    def set_history(self, new_history):
        self.history = new_history[-Config.CALCULATOR_MAX_HISTORY_SIZE :]

    def save_to_csv(self, filename=None):
        filename = filename or Config.HISTORY_FILE
        file_path = Path(filename)

        data = []
        for calc in self.history:
            data.append(
                {
                    "operation": calc.operation,
                    "a": calc.a,
                    "b": calc.b,
                    "result": calc.perform(),
                    "timestamp": getattr(calc, "timestamp", None),
                }
            )

        df = pd.DataFrame(data)

        try:
            df.to_csv(file_path, index=False, encoding=Config.CALCULATOR_DEFAULT_ENCODING)
        except Exception as exc:
            raise PersistenceError(f"Failed to save history to CSV: {exc}") from exc

    def load_from_csv(self, filename=None):
        filename = filename or Config.HISTORY_FILE
        file_path = Path(filename)

        try:
            df = pd.read_csv(file_path, encoding=Config.CALCULATOR_DEFAULT_ENCODING)
        except FileNotFoundError as exc:
            raise PersistenceError("No history file found.") from exc
        except Exception as exc:
            raise PersistenceError(f"Failed to read history CSV: {exc}") from exc

        required_columns = {"operation", "a", "b"}
        if not required_columns.issubset(df.columns):
            raise PersistenceError("Malformed CSV: missing required columns.")

        new_history = []
        try:
            for _, row in df.iterrows():
                calc = Calculation.create(row["operation"], row["a"], row["b"])
                new_history.append(calc)
        except Exception as exc:
            raise PersistenceError(f"Malformed CSV data: {exc}") from exc

        self.set_history(new_history)