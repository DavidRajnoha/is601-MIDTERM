"""Command to delete a calculation from history."""
import logging
from src.command.command import Command
from src.core.logging_decorator import log_class
from src.persistance.calculation_history import CalculationHistory, CalculationHistoryInterface
from src.exceptions.calculation_exceptions import CalculationNotFoundError, InvalidCalculationDataError


@log_class
class DeleteHistoryCommand(Command):
    """Command to delete a specific calculation from history."""

    def __init__(self, history: CalculationHistoryInterface=None):
        self.history = history or CalculationHistory()

    def execute(self, args=None):
        """Execute the delete history command."""
        calc_id = input("Enter the ID of the calculation to delete: ")

        try:
            if not calc_id:
                raise ValueError("Please provide a calculation ID to delete.")

            self.history.delete_calculation(calc_id)
            result = f"Calculation with ID {calc_id} has been deleted."

        except ValueError as e:
            result = f"Error: {str(e)}"
        except CalculationNotFoundError as e:
            result = f"Error: {str(e)}"
        except InvalidCalculationDataError as e:
            result = f"Error: {str(e)}"

        logging.info(result)
        print(result)
        return result