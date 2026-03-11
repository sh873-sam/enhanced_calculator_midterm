"""
Memento classes for saving and restoring calculator history state.
"""

from copy import deepcopy


class CalculatorMemento:
    def __init__(self, history_state):
        self._history_state = deepcopy(history_state)

    def get_state(self):
        return deepcopy(self._history_state)


class HistoryCaretaker:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def save(self, history_state):
        self.undo_stack.append(CalculatorMemento(history_state))
        self.redo_stack.clear()

    def undo(self, current_state):
        if not self.undo_stack:
            return None

        self.redo_stack.append(CalculatorMemento(current_state))
        memento = self.undo_stack.pop()
        return memento.get_state()

    def redo(self, current_state):
        if not self.redo_stack:
            return None

        self.undo_stack.append(CalculatorMemento(current_state))
        memento = self.redo_stack.pop()
        return memento.get_state()