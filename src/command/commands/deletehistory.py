"""Command to delete a specific record from the calculation history."""
import logging

from src.command.command import Command
from src.persistance.calculation_history import CalculationHistory, CalculationHistoryInterface


class DeleteHistoryCommand(Command):
    """Command to delete a specific calculation from history by ID."""

    def __init__(self, history: CalculationHistoryInterface=None):
        self.history = history or CalculationHistory()

    def execute(self):
        """Execute the delete history command."""

        calc_id = input("Enter the ID of the calculation to delete: ")

        if not calc_id:
            result = "Error: Please provide a calculation ID to delete."
            print(result)
            logging.info(result)
            return result

        calculation = self.history.get_calculation_by_id(calc_id)
        if not calculation:
            result = f"Error: No calculation with ID {calc_id} found."
            print(result)
            logging.info(result)
            return result

        self.history.delete_calculation(calc_id)
        result = f"Calculation with ID {calc_id} has been deleted."
        logging.info(result)
        print(result)
        return result