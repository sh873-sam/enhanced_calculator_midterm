"""
Configuration loader for calculator using .env
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    LOG_FILE = os.getenv("LOG_FILE", "calculator.log")
    HISTORY_FILE = os.getenv("HISTORY_FILE", "history.csv")
    AUTO_SAVE = os.getenv("AUTO_SAVE", "true").lower() == "true"
    MAX_HISTORY = int(os.getenv("MAX_HISTORY", "100"))
    PRECISION = int(os.getenv("PRECISION", "4"))