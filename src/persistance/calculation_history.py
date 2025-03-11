"""Module containing the CalculationHistory class for storing calculation history."""
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Callable, Dict, Any
from decimal import Decimal

from src.core.logging_decorator import log_class
from src.core.singleton import singleton
from src.model.calculation import Calculation
from src.persistance.csv_repository import CSVRepository
from src.persistance.memory_repository import MemoryRepository
from src.persistance.repository_interface import RepositoryInterface


class CalculationHistoryInterface(ABC):
    """Interface for managing calculation history."""

    @abstractmethod
    def add_calculation(self, calculation: Calculation) -> None:
        """Add a calculation to the history."""
        pass

    @abstractmethod
    def get_all_calculations(self) -> List[Calculation]:
        """Get all calculations in the history."""
        pass

    @abstractmethod
    def get_calculation_by_id(self, calculation_id: str) -> Optional[Calculation]:
        """Get a calculation by its ID."""
        pass

    @abstractmethod
    def get_last_calculation(self) -> Optional[Calculation]:
        """Get the most recent calculation."""
        pass

    @abstractmethod
    def filter_calculations_by_operation(self, operation_name: str) -> List[Calculation]:
        """Filter calculations by operation name."""
        pass

    @abstractmethod
    def filter_calculations_by_result(self, result: Decimal) -> List[Calculation]:
        """Filter calculations by result value."""
        pass

    @abstractmethod
    def clear_history(self) -> None:
        """Clear all calculation history."""
        pass

    @abstractmethod
    def delete_calculation(self, calculation_id: str) -> bool:
        """Delete a calculation by its ID."""
        pass


@singleton
@log_class
class CalculationHistory(CalculationHistoryInterface):
    """
    Manages the history of calculations in the application.

    This class provides an interface to store, retrieve, and query calculation history
    using a repository implementation. It handles conversion between Calculation objects
    and their dictionary representation used by repositories.
    """

    def __init__(self, repository = None):
        """
        Initialize the calculation history with a repository.

        Args:
            repository: An existing repository instance
        """
        if repository is not None:
            self.repository = repository
        else:
            self.repository = CSVRepository()

    def add_calculation(self, calculation: Calculation) -> None:
        """
        Add a calculation to the history.

        Args:
            calculation: The calculation to add, which should already be executed
        """
        logging.debug(f"Adding calculation to history: {calculation}")
        calculation_dict = Calculation.to_dict(calculation)
        self.repository.add(calculation_dict)

    def get_all_calculations(self) -> List[Calculation]:
        """
        Get all calculations in the history.

        Returns:
            A list of all valid calculations, skipping any with serialization errors
        """
        calculation_dicts = self.repository.get_all()
        result = []

        for calc_dict in calculation_dicts:
            try:
                calculation = Calculation.from_dict(calc_dict)
                result.append(calculation)
            except (ValueError, KeyError) as e:
                logging.warning(f"Skipping invalid calculation: {e}")

        return result

    def get_calculation_by_id(self, calculation_id: str) -> Optional[Calculation]:
        """
        Get a calculation by its ID.

        Args:
            calculation_id: The ID of the calculation to retrieve

        Returns:
            The calculation if found and valid, None otherwise
        """
        calc_dict = self.repository.get_by_id(calculation_id)
        if calc_dict is None:
            return None

        try:
            return Calculation.from_dict(calc_dict)
        except (ValueError, KeyError) as e:
            logging.warning(f"Invalid calculation data for ID {calculation_id}: {e}")
            return None

    def get_last_calculation(self) -> Optional[Calculation]:
        """
        Get the most recent calculation.

        Returns:
            The last calculation added to the history, or None if history is empty
        """
        calc_dict = self.repository.get_last()
        if calc_dict is None:
            return None

        try:
            return Calculation.from_dict(calc_dict)
        except (ValueError, KeyError) as e:
            logging.warning(f"Invalid data for last calculation: {e}")
            return None

    def filter_calculations_by_operation(self, operation_name: str) -> List[Calculation]:
        """
        Filter calculations by operation name.

        Args:
            operation_name: The name of the operation to filter by

        Returns:
            A list of calculations with the specified operation name
        """
        all_calculations = self.get_all_calculations()
        return [
            calc for calc in all_calculations
            if calc.operation_name == operation_name
        ]

    def filter_calculations_by_result(self, result: Decimal) -> List[Calculation]:
        """
        Filter calculations by result value.

        Args:
            result: The exact result value to filter by

        Returns:
            A list of calculations with the specified result
        """
        all_calculations = self.get_all_calculations()
        return [
            calc for calc in all_calculations
            if calc.result == result
        ]
        
    def clear_history(self) -> None:
        """Clear all calculation history."""
        logging.debug("Clearing calculation history")
        self.repository.clear()
        
    def delete_calculation(self, calculation_id: str) -> bool:
        """
        Delete a calculation from history by its ID.
        
        Args:
            calculation_id: The ID of the calculation to delete
            
        Returns:
            bool: True if calculation was deleted, False otherwise
        """
        logging.debug(f"Deleting calculation with ID: {calculation_id}")
        return self.repository.delete(calculation_id)