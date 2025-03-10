from src.core.singleton import singleton
from src.model.calculation import Calculation
from src.persistance.calculation_history import CalculationHistoryInterface, CalculationHistory
from decimal import Decimal

import logging

@singleton
class Calculator:
    """
    Calculator class that uses a Singleton pattern.
    It performs operations on two numbers and stores the history of calculations.
    """
    def __init__(self, history: CalculationHistoryInterface=None):
        self._history = history or CalculationHistory()

    def perform_operation(self, operation, a: Decimal, b: Decimal) -> Decimal:
        logging.debug(f"Performing operation: {operation.__name__}({a}, {b})")
        calculation = Calculation(operation, a, b)
        self._history.add_calculation(calculation)
        return calculation.perform_operation()