"""Module containing the CalculationHistory class for storing calculation history."""
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from decimal import Decimal

from src.core.logging_decorator import log_class
from src.core.singleton import singleton
from src.model.calculation import Calculation
from src.persistance.csv_repository import CSVRepository
from src.persistance.repository_interface import RepositoryInterface
from src.exceptions.calculation_exceptions import (
    CalculationNotFoundError,
    EmptyHistoryError,
    InvalidCalculationDataError
)
from src.exceptions.repository_exceptions import (
    ItemNotFoundError,
    EmptyRepositoryError,
    RepositoryIOError
)


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
    def get_calculation_by_id(self, calculation_id: str) -> Calculation:
        """Get a calculation by its ID."""
        pass

    @abstractmethod
    def get_last_calculation(self) -> Calculation:
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
    def delete_calculation(self, calculation_id: str) -> None:
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

    def __init__(self, repository: RepositoryInterface[Dict[str, Any]] = None):
        """
        Initialize the calculation history with a repository.

        Args:
            repository: An existing repository instance
        """
        self.repository = repository if repository is not None else CSVRepository()

    def add_calculation(self, calculation: Calculation) -> None:
        """
        Add a calculation to the history.

        Args:
            calculation: The calculation to add, which should already be executed

        Raises:
            RepositoryIOError: If there's an error adding the calculation to the repository
        """
        self.logger.info(f"Adding calculation to history: {calculation}")
        try:
            calculation_dict = Calculation.to_dict(calculation)
            self.repository.add(calculation_dict)
        except RepositoryIOError as e:
            self.logger.error(f"Error adding calculation to history: {e}")
            raise

    def get_all_calculations(self) -> List[Calculation]:
        """
        Get all calculations in the history.

        Returns:
            A list of all valid calculations, skipping any with serialization errors

        Raises:
            EmptyHistoryError: If the history is empty
        """
        try:
            calculation_dicts = self.repository.get_all()
            result = []

            for calc_dict in calculation_dicts:
                try:
                    calculation = Calculation.from_dict(calc_dict)
                    result.append(calculation)
                except (ValueError, KeyError) as e:
                    self.logger.warning(f"Skipping invalid calculation: {e}")

            return result

        except EmptyRepositoryError:
            raise EmptyHistoryError()
        except RepositoryIOError as e:
            self.logger.error(f"Error retrieving calculations: {e}")
            raise

    def get_calculation_by_id(self, calculation_id: str) -> Calculation:
        """
        Get a calculation by its ID.

        Args:
            calculation_id: The ID of the calculation to retrieve

        Returns:
            The calculation if found and valid

        Raises:
            CalculationNotFoundError: If no calculation with the given ID exists
            InvalidCalculationDataError: If the calculation data is invalid
        """
        try:
            calc_dict = self.repository.get_by_id(calculation_id)

            try:
                return Calculation.from_dict(calc_dict)
            except (ValueError, KeyError) as e:
                self.logger.warning(f"Invalid calculation data: {e}")
                raise InvalidCalculationDataError(calculation_id, e)

        except ItemNotFoundError:
            raise CalculationNotFoundError(calculation_id)
        except RepositoryIOError as e:
            self.logger.error(f"Error retrieving calculation {calculation_id}: {e}")
            raise

    def get_last_calculation(self) -> Calculation:
        """
        Get the most recent calculation.

        Returns:
            The last calculation added to the history

        Raises:
            EmptyHistoryError: If the history is empty
            InvalidCalculationDataError: If the calculation data is invalid
        """
        try:
            calc_dict = self.repository.get_last()

            try:
                return Calculation.from_dict(calc_dict)
            except (ValueError, KeyError) as e:
                raise InvalidCalculationDataError(error=e)

        except EmptyRepositoryError:
            raise EmptyHistoryError()
        except RepositoryIOError as e:
            self.logger.error(f"Error retrieving last calculation: {e}")
            raise

    def filter_calculations_by_operation(self, operation_name: str) -> List[Calculation]:
        """
        Filter calculations by operation name.

        Args:
            operation_name: The name of the operation to filter by

        Returns:
            A list of calculations with the specified operation name
        """
        try:
            all_calculations = self.get_all_calculations()
            return [
                calc for calc in all_calculations
                if calc.operation_name == operation_name
            ]
        except EmptyHistoryError:
            return []
        except RepositoryIOError as e:
            self.logger.error(f"Error filtering calculations: {e}")
            raise

    def filter_calculations_by_result(self, result: Decimal) -> List[Calculation]:
        """
        Filter calculations by result value.

        Args:
            result: The exact result value to filter by

        Returns:
            A list of calculations with the specified result
        """
        try:
            all_calculations = self.get_all_calculations()
            return [
                calc for calc in all_calculations
                if calc.result == result
            ]
        except EmptyHistoryError:
            return []
        except RepositoryIOError as e:
            self.logger.error(f"Error filtering calculations: {e}")
            raise

    def clear_history(self) -> None:
        """
        Clear all calculation history.

        Raises:
            RepositoryIOError: If there's an error clearing the history
        """
        self.logger.info("Clearing calculation history")
        try:
            self.repository.clear()
        except RepositoryIOError as e:
            self.logger.error(f"Error clearing history: {e}")
            raise

    def delete_calculation(self, calculation_id: str) -> None:
        """
        Delete a calculation from history by its ID.

        Args:
            calculation_id: The ID of the calculation to delete

        Raises:
            CalculationNotFoundError: If no calculation with the given ID exists
            RepositoryIOError: If there's an error deleting the calculation
        """
        self.logger.info(f"Deleting calculation with ID: {calculation_id}")
        try:
            self.repository.delete(calculation_id)
        except ItemNotFoundError:
            raise CalculationNotFoundError(calculation_id)
        except RepositoryIOError as e:
            self.logger.error(f"Error deleting calculation {calculation_id}: {e}")
            raise