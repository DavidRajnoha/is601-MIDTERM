"""Module containing custom exceptions for the calculator application."""


class CalculationError(Exception):
    """Base exception for calculation-related errors."""
    pass


class CalculationNotFoundError(CalculationError):
    """Exception raised when a calculation cannot be found."""

    def __init__(self, calculation_id: str):
        self.calculation_id = calculation_id
        self.message = f"No calculation with ID {calculation_id} found."
        super().__init__(self.message)


class EmptyHistoryError(CalculationError):
    """Exception raised when trying to access history that is empty."""

    def __init__(self):
        self.message = "History is empty."
        super().__init__(self.message)


class InvalidCalculationDataError(CalculationError):
    """Exception raised when calculation data is invalid."""

    def __init__(self, calculation_id: str = None, error: Exception = None):
        self.calculation_id = calculation_id
        self.error = error
        if calculation_id:
            self.message = f"Invalid calculation data for ID {calculation_id}: {error}"
        else:
            self.message = f"Invalid calculation data: {error}"
        super().__init__(self.message)