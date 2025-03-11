from src.core.logging_decorator import log_class
from src.core.singleton import singleton
from src.model.calculation import Calculation
from src.persistance.calculation_history import CalculationHistoryInterface, CalculationHistory
from decimal import Decimal

import logging

@singleton
@log_class
class Calculator:
    """
    Calculator class that uses a Singleton pattern.
    It performs operations on two numbers and stores the history of calculations.
    """
    def __init__(self, history: CalculationHistoryInterface=None):
        self._history = history or CalculationHistory()

    def perform_operation(self, operation, a: Decimal, b: Decimal) -> Decimal:
        calculation = Calculation(operation, a, b)
        result = calculation.perform_operation()
        self._history.add_calculation(calculation)
        return result