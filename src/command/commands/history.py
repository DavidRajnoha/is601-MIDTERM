"""Command to display calculation history."""
from src.command.command import Command
from src.core.logging_decorator import log_class
from src.persistance.calculation_history import CalculationHistory, CalculationHistoryInterface


@log_class
class HistoryCommand(Command):
    """Command to display the calculation history."""

    def __init__(self, history: CalculationHistoryInterface=None):
        self.history = history or CalculationHistory()

    def execute(self, args=None):
        """Execute the history command."""
        calculations = self.history.get_all_calculations()
        
        if not calculations:
            result = "History is empty."
            return result

        result = "Calculation History:\n"
        for calc in calculations:
            result += f"ID: {calc.id}, Operation: {calc.operation_name}, " \
                     f"Operands: {calc.operands}, Result: {calc.result}\n"

        print(result)
        return result
