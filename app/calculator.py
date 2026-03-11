"""
Interactive calculator CLI.
"""

from colorama import Fore, Style, init

from app.calculation import Calculation
from app.history import History
from app.input_validators import validate_number, validate_operation

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

    def run(self):
        print(Fore.GREEN + "Enhanced Calculator")
        print("Type 'exit' to quit.\n")

        while True:

            user_input = input(Fore.CYAN + "Enter operation and two numbers: ")

            if user_input.lower() == "exit":
                print(Fore.YELLOW + "Goodbye!")
                break

            try:

                parts = user_input.split()

                if len(parts) != 3:
                    raise ValueError("Format: operation number number")

                operation = validate_operation(parts[0], VALID_OPERATIONS)
                a = validate_number(parts[1])
                b = validate_number(parts[2])

                calculation = Calculation(operation, a, b)

                result = calculation.perform()

                self.history.add(calculation)

                print(Fore.GREEN + f"Result: {result}")

            except Exception as e:
                print(Fore.RED + f"Error: {e}")