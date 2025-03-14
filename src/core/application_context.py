"""
Module for configuring application-wide dependencies.
"""
import logging

from src.core.logging_decorator import log_class
from src.persistance.csv_repository import CSVRepository
from src.persistance.memory_repository import MemoryRepository
from src.persistance.calculation_history import CalculationHistory

@log_class
class ApplicationContext:
    """
    Utility class for configuring application-wide dependencies.
    Contains only static methods for initializing and configuring singletons.
    """

    @staticmethod
    def configure_repositories(repository_type="csv", file_path="data/calculations.csv"):
        """
        Configure repository singletons used in the application.

        Args:
            repository_type: Type of repository to use ("csv" or "memory")
            file_path: Path to the CSV file when using CSV repository
        """
        logging.info(f"Configuring repositories: type={repository_type}, file_path={file_path}")

        ApplicationContext._reset_repository_singletons()

        repository = ApplicationContext._create_repository(repository_type, file_path)

        CalculationHistory(repository=repository)
        logging.debug("Calculation history configured")

    @staticmethod
    def _reset_repository_singletons():
        """Reset repository-related singleton instances."""
        CSVRepository.reset_instance()
        MemoryRepository.reset_instance()
        CalculationHistory.reset_instance()

    @staticmethod
    def _create_repository(repository_type, file_path):
        """Create and return the appropriate repository instance."""
        if repository_type.lower() == "csv":
            repository = CSVRepository(file_path)
            logging.debug(f"Using CSV repository with file: {file_path}")
        else:
            repository = MemoryRepository()
            logging.debug("Using in-memory repository")

        return repository
