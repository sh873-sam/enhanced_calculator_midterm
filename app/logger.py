"""
Observer classes for calculator logging and auto-save.
"""

import logging

from app.calculator_config import Config


class LoggingObserver:
    """
    Logs every calculation to a log file.
    """

    def __init__(self, log_file=Config.LOG_FILE):
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            force=True,
            encoding=Config.CALCULATOR_DEFAULT_ENCODING,
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
    """
    Automatically saves calculator history to CSV after each calculation.
    """

    def __init__(self, history, filename=Config.HISTORY_FILE):
        self.history = history
        self.filename = filename

    def update(self, calculation):
        if Config.CALCULATOR_AUTO_SAVE:
            self.history.save_to_csv(self.filename)