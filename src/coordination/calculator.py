from src.core.logging_decorator import log_class
from src.core.singleton import singleton
from src.model.calculation import Calculation
from src.persistance.calculation_history import CalculationHistoryInterface, CalculationHistory
from decimal import Decimal

@singleton
@log_class
class Calculator:
    """
    Calculator class that uses a Singleton pattern.
    It performs operations on two numbers and stores the history of calculations.
    """
    def __init__(self, history: CalculationHistoryInterface=None):
        self._history = history or CalculationHistory()
        self.logger.debug("Calculator initialized")

    def perform_operation(self, operation, a: Decimal, b: Decimal) -> Decimal:
        operation_name = operation.__name__ if hasattr(operation, "__name__") else "unknown"
        self.logger.debug(f"Performing {operation_name} operation with {a} and {b}")
        
        calculation = Calculation(operation, a, b)
        result = calculation.perform_operation()
        
        self._history.add_calculation(calculation)
        self.logger.debug(f"Operation result: {result}")
        return result