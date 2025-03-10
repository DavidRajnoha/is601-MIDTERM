"""Module containing the CalculationHistory class for storing calculation history."""
import logging
from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal

from src.core.logging import log_class
from src.core.singleton import singleton
from src.model.calculation import Calculation
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


@singleton
@log_class
class CalculationHistory(CalculationHistoryInterface):
    """
    Manages the history of calculations in the application.
    
    This class provides an interface to store, retrieve, and query calculation history
    using a repository implementation without modifying or executing the calculations.
    """
    
    def __init__(self, repository: RepositoryInterface[Calculation] = None):
        """
        Initialize the calculation history with a repository.
        
        Args:
            repository: A repository implementation for storing calculations
        """
        self.repository = repository or MemoryRepository()

    def add_calculation(self, calculation: Calculation) -> None:
        """
        Add a calculation to the history.
        
        Args:
            calculation: The calculation to add, which should already be executed
        """
        logging.debug(f"Adding calculation to history: {calculation}")
        self.repository.add(calculation)
        
    def get_all_calculations(self) -> List[Calculation]:
        """
        Get all calculations in the history.
        
        Returns:
            A list of all calculations
        """
        return self.repository.get_all()
        
    def get_calculation_by_id(self, calculation_id: str) -> Optional[Calculation]:
        """
        Get a calculation by its ID.
        
        Args:
            calculation_id: The ID of the calculation to retrieve
            
        Returns:
            The calculation if found, None otherwise
        """
        return self.repository.get_by_id(calculation_id)
        
    def get_last_calculation(self) -> Optional[Calculation]:
        """
        Get the most recent calculation.
        
        Returns:
            The last calculation added to the history, or None if history is empty
        """
        return self.repository.get_last()
        
    def filter_calculations_by_operation(self, operation_name: str) -> List[Calculation]:
        """
        Filter calculations by operation name.
        
        Args:
            operation_name: The name of the operation to filter by
            
        Returns:
            A list of calculations with the specified operation name
        """
        return self.repository.filter(
            lambda calc: calc.operation_name == operation_name
        )
        
    def filter_calculations_by_result(self, result: Decimal) -> List[Calculation]:
        """
        Filter calculations by result value.
        
        Args:
            result: The exact result value to filter by
            
        Returns:
            A list of calculations with the specified result
        """
        return self.repository.filter(
            lambda calc: calc.result == result
        )
        
    def clear_history(self) -> None:
        """Clear all calculation history."""
        logging.debug("Clearing calculation history")
        self.repository.clear()