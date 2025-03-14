"""Command to clear the calculation history."""
from src.command.command import Command
from src.persistance.calculation_history import CalculationHistoryInterface, CalculationHistory


class ClearHistoryCommand(Command):
    """Command to clear the entire calculation history."""

    def __init__(self, history: CalculationHistoryInterface=None):
        self.history = history or CalculationHistory()

    def execute(self, args=None):
        """Execute the clear history command."""
        self.history.clear_history()
        result = "Calculation history has been cleared."
        print(result)
        return result