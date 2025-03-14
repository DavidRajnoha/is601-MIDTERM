"""
This module contains the OperationExecutor class, which encapsulates the shared logic for executing an operation.
"""
from decimal import Decimal, InvalidOperation
from src.coordination.calculator import Calculator

from src.core.logging_decorator import log_class


def _get_decimal_input(prompt: str) -> Decimal:
    raw_input = input(prompt)
    return Decimal(raw_input)

@log_class
class BinaryOperationExecutor:
    """
    Encapsulates the shared logic for executing an operation:
      - Reading two decimal inputs from the user.
      - Executing the provided operation.
      - Handling errors and displaying results.
    """
    def __init__(self, operation_callable, operation_name: str, calculator: Calculator = None):
        self.calculator = calculator or Calculator()
        self.operation_callable = operation_callable
        self.operation_name = operation_name
        self.logger.debug(f"BinaryOperationExecutor created for {operation_name}")

    def execute(self):
        """
        Executes the operation by reading two decimal inputs from the user and displaying the result.
        """
        try:
            a = _get_decimal_input("Enter the first number: ")
            b = _get_decimal_input("Enter the second number: ")
            self.logger.debug(f"Read inputs: {a}, {b}")
        except (InvalidOperation, ValueError):
            self.logger.info("Invalid input provided by user")
            print("Invalid input. Please enter valid decimal numbers.")
            return

        try:
            self.logger.debug(f"Executing {self.operation_name} operation with inputs: {a}, {b}")
            result = self.calculator.perform_operation(self.operation_callable, a, b)
            print(f"Result of {self.operation_name}: {result}")
            self.logger.info(f"User executed {self.operation_name} operation: {a} {self.operation_name} {b} = {result}")
        except ZeroDivisionError:
            self.logger.info(f"User executed {self.operation_name} operation: {a} {self.operation_name} {b} which "
                             f"resulted in division by zero")
            print("The result of division by zero is not defined.")
        except Exception as e:
            self.logger.error(f"Unexpected error during {self.operation_name} operation: {e}")
            print(f"An error occurred.")

