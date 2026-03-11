# Enhanced Calculator Midterm

## Project Overview

This project is an enhanced command-line calculator built in Python. It supports standard and advanced arithmetic operations, history tracking, undo/redo functionality, logging, CSV persistence, configuration through environment variables, automated testing, and CI with GitHub Actions.

The application was designed to demonstrate object-oriented programming, design patterns, error handling, persistence, and test automation.

---

## Features

### Arithmetic Operations
The calculator supports the following operations:

- `add`
- `subtract`
- `multiply`
- `divide`
- `power`
- `root`
- `modulus`
- `int_divide`
- `percent`
- `abs_diff`

### Command-Line Commands
The calculator also supports these commands:

- `history` — display calculation history
- `clear` — clear history
- `undo` — undo the last action
- `redo` — redo the last undone action
- `save` — save history to CSV
- `load` — load history from CSV
- `help` — show available commands
- `exit` — quit the program

---

## Design Patterns Used

### Factory Pattern
The calculator uses a factory-style creation approach through `Calculation.create()` to validate and create calculation objects based on the requested operation.

### Memento Pattern
Undo and redo functionality are implemented using the Memento pattern through `CalculatorMemento` and `HistoryCaretaker`.

### Observer Pattern
The calculator uses observers to respond automatically after new calculations are performed:

- `LoggingObserver` writes calculation details to a log file
- `AutoSaveObserver` automatically saves history to CSV

---

## Project Structure

```text
project_root/
├── app/
│   ├── __init__.py
│   ├── calculator.py
│   ├── calculation.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   ├── logger.py
│   └── operations.py
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_calculation.py
│   └── test_operations.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── .github/
    └── workflows/
        └── python-app.yml
