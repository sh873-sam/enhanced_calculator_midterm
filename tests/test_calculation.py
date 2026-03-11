import pytest

from app.calculation import Calculation
from app.calculator_memento import HistoryCaretaker
from app.history import History
from app.input_validators import validate_number
from app.exceptions import OperationError, ValidationError, PersistenceError


def test_calculation_perform_add():
    calc = Calculation("add", 2, 3)
    assert calc.perform() == 5


def test_calculation_perform_subtract():
    calc = Calculation("subtract", 10, 4)
    assert calc.perform() == 6


def test_calculation_perform_multiply():
    calc = Calculation("multiply", 3, 5)
    assert calc.perform() == 15


def test_calculation_perform_divide():
    calc = Calculation("divide", 10, 2)
    assert calc.perform() == 5


def test_calculation_invalid_operation():
    with pytest.raises(OperationError, match="Invalid operation: unknown"):
        Calculation.create("unknown", 1, 2)


# -------------------------
# New coverage tests
# -------------------------

def test_validate_number_exceeds_max():
    with pytest.raises(ValidationError, match="Input exceeds maximum allowed value"):
        validate_number("1000001")


def test_history_max_size_limit():
    history = History()

    for i in range(105):
        history.add(Calculation("add", i, 1))

    assert len(history.get_all()) == 100


def test_history_set_history_respects_max_size():
    history = History()
    large_history = [Calculation("add", i, 1) for i in range(150)]

    history.set_history(large_history)

    assert len(history.get_all()) == 100


def test_history_save_to_csv_failure(monkeypatch, tmp_path):
    history = History()
    history.add(Calculation("add", 2, 3))

    def fake_to_csv(*args, **kwargs):
        raise Exception("write failed")

    monkeypatch.setattr("pandas.DataFrame.to_csv", fake_to_csv)

    with pytest.raises(PersistenceError, match="Failed to save history to CSV"):
        history.save_to_csv(tmp_path / "bad.csv")


def test_history_load_from_csv_file_not_found(tmp_path):
    history = History()

    with pytest.raises(PersistenceError, match="No history file found"):
        history.load_from_csv(tmp_path / "missing.csv")


def test_history_load_from_csv_missing_columns(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("x,y,z\n1,2,3\n", encoding="utf-8")

    history = History()

    with pytest.raises(PersistenceError, match="Malformed CSV: missing required columns"):
        history.load_from_csv(bad_csv)


def test_history_load_from_csv_bad_data(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("operation,a,b\nunknown,1,2\n", encoding="utf-8")

    history = History()

    with pytest.raises(PersistenceError, match="Malformed CSV data"):
        history.load_from_csv(bad_csv)


def test_history_caretaker_redo_empty_after_save():
    caretaker = HistoryCaretaker()
    caretaker.save([Calculation("add", 1, 2)])

    assert caretaker.redo([]) is None


def test_history_caretaker_save_clears_redo_stack():
    caretaker = HistoryCaretaker()

    state1 = [Calculation("add", 1, 2)]
    current_state = [Calculation("add", 1, 2), Calculation("multiply", 2, 3)]

    caretaker.save(state1)
    caretaker.undo(current_state)

    assert len(caretaker.redo_stack) == 1

    caretaker.save(current_state)

    assert len(caretaker.redo_stack) == 0