"""
Interactive calculator CLI.
"""

from colorama import Fore, init

from app.calculation import Calculation
from app.history import History
from app.input_validators import validate_number, validate_operation
from app.calculator_memento import HistoryCaretaker
from app.logger import LoggingObserver, AutoSaveObserver

init(autoreset=True)

VALID_OPERATIONS = {
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "root",
    "modulus",
    "int_divide",
    "percent",
    "abs_diff",
}


class Calculator:
    def __init__(self):
        self.history = History()
        self.caretaker = HistoryCaretaker()
        self.observers = [
            LoggingObserver(),
            AutoSaveObserver(self.history),
        ]

    def notify_observers(self, calculation):
        for observer in self.observers:
            observer.update(calculation)

    def run(self):
        print(Fore.GREEN + "Enhanced Calculator")
        print("Commands: history, clear, undo, redo, save, load, help, exit")
        print("For math: operation number number\n")

        while True:
            user_input = input(Fore.CYAN + "Enter operation and two numbers: ").strip()

            if user_input.lower() == "exit":
                print(Fore.YELLOW + "Goodbye!")
                break

            if user_input.lower() == "help":
                print(Fore.YELLOW + "Available operations:")
                print(", ".join(sorted(VALID_OPERATIONS)))
                print("Other commands: history, clear, undo, redo, save, load, help, exit")
                continue

            if user_input.lower() == "history":
                if not self.history.get_all():
                    print(Fore.YELLOW + "History is empty.")
                else:
                    for i, calc in enumerate(self.history.get_all(), start=1):
                        print(
                            Fore.YELLOW
                            + f"{i}. {calc.operation} {calc.a} {calc.b} = {calc.perform()}"
                        )
                continue

            if user_input.lower() == "clear":
                self.caretaker.save(self.history.get_all())
                self.history.clear()
                print(Fore.YELLOW + "History cleared.")
                continue

            if user_input.lower() == "undo":
                previous_state = self.caretaker.undo(self.history.get_all())
                if previous_state is None:
                    print(Fore.RED + "Nothing to undo.")
                else:
                    self.history.set_history(previous_state)
                    print(Fore.YELLOW + "Undo successful.")
                continue

            if user_input.lower() == "redo":
                next_state = self.caretaker.redo(self.history.get_all())
                if next_state is None:
                    print(Fore.RED + "Nothing to redo.")
                else:
                    self.history.set_history(next_state)
                    print(Fore.YELLOW + "Redo successful.")
                continue

            if user_input.lower() == "save":
                self.history.save_to_csv()
                print(Fore.YELLOW + "History saved to CSV.")
                continue

            if user_input.lower() == "load":
                try:
                    self.history.load_from_csv()
                    print(Fore.YELLOW + "History loaded from CSV.")
                except FileNotFoundError:
                    print(Fore.RED + "No history file found.")
                continue

            try:
                parts = user_input.split()

                if len(parts) != 3:
                    raise ValueError("Format: operation number number")

                operation = validate_operation(parts[0], VALID_OPERATIONS)
                a = validate_number(parts[1])
                b = validate_number(parts[2])

                self.caretaker.save(self.history.get_all())

                calculation = Calculation(operation, a, b)
                result = calculation.perform()
                self.history.add(calculation)
                self.notify_observers(calculation)

                print(Fore.GREEN + f"Result: {result}")

            except Exception as e:
                print(Fore.RED + f"Error: {e}")


if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()