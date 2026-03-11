import importlib
from pathlib import Path

from app.calculator import Calculator
import app.calculator_config as calculator_config
from app.calculation import Calculation
from app.history import History
from app.logger import LoggingObserver, AutoSaveObserver


def test_help_command(monkeypatch, capsys):
    inputs = iter(["help", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calc = Calculator()
    calc.run()

    captured = capsys.readouterr()
    assert "Available operations:" in captured.out
    assert "exit" in captured.out


def test_history_empty(monkeypatch, capsys):
    inputs = iter(["history", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calc = Calculator()
    calc.run()

    captured = capsys.readouterr()
    assert "History is empty." in captured.out


def test_undo_when_empty(monkeypatch, capsys):
    inputs = iter(["undo", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calc = Calculator()
    calc.run()

    captured = capsys.readouterr()
    assert "Nothing to undo." in captured.out


def test_redo_when_empty(monkeypatch, capsys):
    inputs = iter(["redo", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calc = Calculator()
    calc.run()

    captured = capsys.readouterr()
    assert "Nothing to redo." in captured.out


def test_invalid_format(monkeypatch, capsys):
    inputs = iter(["add 2", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calc = Calculator()
    calc.run()

    captured = capsys.readouterr()
    assert "Format: operation number number" in captured.out


def test_invalid_operation(monkeypatch, capsys):
    inputs = iter(["unknown 2 3", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calc = Calculator()
    calc.run()

    captured = capsys.readouterr()
    assert "Invalid operation: unknown" in captured.out


def test_add_operation(monkeypatch, capsys):
    inputs = iter(["add 2 3", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calc = Calculator()
    calc.run()

    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out


def test_clear_command(monkeypatch, capsys):
    inputs = iter(["add 2 3", "clear", "history", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calc = Calculator()
    calc.run()

    captured = capsys.readouterr()
    assert "History cleared." in captured.out
    assert "History is empty." in captured.out


def test_save_and_load_commands(monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)

    inputs = iter(["add 2 3", "save", "clear", "load", "history", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calc = Calculator()
    calc.run()

    captured = capsys.readouterr()
    assert "History saved to CSV." in captured.out
    assert "History loaded from CSV." in captured.out
    assert "add 2.0 3.0 = 5.0" in captured.out


def test_config_defaults(monkeypatch):
    monkeypatch.delenv("LOG_FILE", raising=False)
    monkeypatch.delenv("HISTORY_FILE", raising=False)
    monkeypatch.delenv("AUTO_SAVE", raising=False)
    monkeypatch.delenv("MAX_HISTORY", raising=False)
    monkeypatch.delenv("PRECISION", raising=False)

    importlib.reload(calculator_config)

    assert calculator_config.Config.LOG_FILE == "calculator.log"
    assert calculator_config.Config.HISTORY_FILE == "history.csv"
    assert calculator_config.Config.AUTO_SAVE is True
    assert calculator_config.Config.MAX_HISTORY == 100
    assert calculator_config.Config.PRECISION == 4


def test_config_env_values(monkeypatch):
    monkeypatch.setenv("LOG_FILE", "custom.log")
    monkeypatch.setenv("HISTORY_FILE", "custom.csv")
    monkeypatch.setenv("AUTO_SAVE", "false")
    monkeypatch.setenv("MAX_HISTORY", "50")
    monkeypatch.setenv("PRECISION", "2")

    importlib.reload(calculator_config)

    assert calculator_config.Config.LOG_FILE == "custom.log"
    assert calculator_config.Config.HISTORY_FILE == "custom.csv"
    assert calculator_config.Config.AUTO_SAVE is False
    assert calculator_config.Config.MAX_HISTORY == 50
    assert calculator_config.Config.PRECISION == 2


def test_logging_observer_creates_log_file(tmp_path):
    log_file = tmp_path / "test_calculator.log"
    observer = LoggingObserver(log_file=str(log_file))
    calculation = Calculation("add", 2, 3)

    observer.update(calculation)

    assert log_file.exists()


def test_autosave_observer_creates_csv(tmp_path):
    history = History()
    calculation = Calculation("add", 2, 3)
    history.add(calculation)

    csv_file = tmp_path / "test_history.csv"
    observer = AutoSaveObserver(history, filename=str(csv_file))

    observer.update(calculation)

    assert csv_file.exists()