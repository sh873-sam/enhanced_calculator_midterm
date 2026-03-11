"""
Configuration loader and validator for calculator using .env
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from app.exceptions import ValidationError

load_dotenv()


class Config:
    CALCULATOR_LOG_DIR = os.getenv("CALCULATOR_LOG_DIR", "logs")
    CALCULATOR_HISTORY_DIR = os.getenv("CALCULATOR_HISTORY_DIR", "data")
    CALCULATOR_MAX_HISTORY_SIZE = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100"))
    CALCULATOR_AUTO_SAVE = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true"
    CALCULATOR_PRECISION = int(os.getenv("CALCULATOR_PRECISION", "4"))
    CALCULATOR_MAX_INPUT_VALUE = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000"))
    CALCULATOR_DEFAULT_ENCODING = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")

    LOG_FILE = str(Path(CALCULATOR_LOG_DIR) / "calculator.log")
    HISTORY_FILE = str(Path(CALCULATOR_HISTORY_DIR) / "history.csv")

    @classmethod
    def validate(cls):
        if cls.CALCULATOR_MAX_HISTORY_SIZE <= 0:
            raise ValidationError("CALCULATOR_MAX_HISTORY_SIZE must be greater than 0.")

        if cls.CALCULATOR_PRECISION < 0:
            raise ValidationError("CALCULATOR_PRECISION must be 0 or greater.")

        if cls.CALCULATOR_MAX_INPUT_VALUE <= 0:
            raise ValidationError("CALCULATOR_MAX_INPUT_VALUE must be greater than 0.")

        if not cls.CALCULATOR_DEFAULT_ENCODING:
            raise ValidationError("CALCULATOR_DEFAULT_ENCODING cannot be empty.")

        Path(cls.CALCULATOR_LOG_DIR).mkdir(parents=True, exist_ok=True)
        Path(cls.CALCULATOR_HISTORY_DIR).mkdir(parents=True, exist_ok=True)