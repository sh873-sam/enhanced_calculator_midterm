"""
Observer classes for calculator logging and auto-save.
"""

import logging


class LoggingObserver:
    def __init__(self, log_file="calculator.log"):
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def update(self, calculation):
        logging.info(
            "Operation=%s, a=%s, b=%s, result=%s",
            calculation.operation,
            calculation.a,
            calculation.b,
            calculation.perform(),
        )


class AutoSaveObserver:
    def __init__(self, history, filename="history.csv"):
        self.history = history
        self.filename = filename

    def update(self, calculation):
        self.history.save_to_csv(self.filename)