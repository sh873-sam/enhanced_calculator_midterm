"""
Manages calculation history and persistence.
"""

import pandas as pd
from datetime import datetime


class History:

    def __init__(self):
        self.history = []

    def add(self, calculation):
        calculation.timestamp = datetime.now()
        self.history.append(calculation)

    def get_all(self):
        return self.history

    def clear(self):
        self.history.clear()

    def last(self):
        if not self.history:
            return None
        return self.history[-1]

    def set_history(self, new_history):
        self.history = new_history

    def save_to_csv(self, filename="history.csv"):
        data = []

        for calc in self.history:
            data.append({
                "operation": calc.operation,
                "a": calc.a,
                "b": calc.b,
                "result": calc.perform(),
                "timestamp": getattr(calc, "timestamp", None)
            })

        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

    def load_from_csv(self, filename="history.csv"):
        df = pd.read_csv(filename)

        from app.calculation import Calculation

        new_history = []

        for _, row in df.iterrows():
            calc = Calculation(row["operation"], row["a"], row["b"])
            new_history.append(calc)

        self.history = new_history