"""
Manages calculation history.
"""

class History:
    def __init__(self):
        self.history = []

    def add(self, calculation):
        self.history.append(calculation)

    def get_all(self):
        return self.history

    def clear(self):
        self.history.clear()

    def last(self):
        if not self.history:
            return None
        return self.history[-1]