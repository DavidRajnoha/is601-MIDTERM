"""
This module contains fixtures that are used by multiple test modules.
"""
# pylint: disable=unused-argument
# pylint: disable=no-member
from typing import Generic, TypeVar, List, Optional, Callable
import pytest

from src.persistance.calculation_history import CalculationHistory
from src.persistance.memory_repository import MemoryRepository

T = TypeVar('T')


@pytest.fixture
def mock_repository():
    """
    Fixture that provides a mock repository instance for testing.

    The MockRepository class is defined within the fixture to keep it
    private to the fixture and hidden from other code.

    Returns:
        An instance of a mock repository implementing RepositoryInterface
    """

    class MockRepository(Generic[T]):
        """
        A minimal mock implementation of the RepositoryInterface for testing purposes.
        All methods do nothing or return empty/default values.
        """

        def add(self, item: T) -> None:
            """Mock add that does nothing."""

        def get_all(self) -> List[T]:
            """Mock get_all that returns empty list."""
            return []

        def get_by_id(self, record_id: str) -> Optional[T]:
            """Mock get_by_id that returns None."""
            return None

        def get_last(self) -> Optional[T]:
            """Mock get_last that returns None."""
            return None

        def filter(self, predicate: Callable[[T], bool]) -> List[T]:
            """Mock filter that returns empty list."""
            return []

        def clear(self) -> None:
            """Mock clear that does nothing."""

    return MockRepository()

@pytest.fixture(autouse=True, scope="function")
def reset_history_after_test():
    """Reset the repository singleton after each test."""
    yield  # Run the test
    MemoryRepository.reset_instance()
    CalculationHistory.reset_instance()
