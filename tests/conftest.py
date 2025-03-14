"""
This module contains fixtures that are used by multiple test modules.
"""
# pylint: disable=unused-argument
# pylint: disable=no-member
from typing import List, Callable, Dict, Any, TypeVar
import pytest

from src.exceptions.repository_exceptions import ItemNotFoundError, EmptyRepositoryError
from src.persistance.calculation_history import CalculationHistory
from src.persistance.memory_repository import MemoryRepository

T = TypeVar('T')


class MockRepository:
    """Mock repository that can be configured to fail for testing error handling."""

    def __init__(self):
        self._items = []
        self.fail_on_get_all = False

    def add(self, item: Dict[str, Any]) -> None:
        """Add an item to the repository."""
        self._items.append(item)

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all items, with option to simulate corrupted data."""
        if not self._items:
            raise EmptyRepositoryError()

        if self.fail_on_get_all:
            return [{"corrupted": "data"}]  # Missing required fields
        return self._items.copy()

    def get_by_id(self, id_: str) -> Dict[str, Any]:
        """Get an item by its ID."""
        for item in self._items:
            if 'id' in item and item['id'] == id_:
                return item
        raise ItemNotFoundError(id_)

    def get_last(self) -> Dict[str, Any]:
        """Get the last item added to the repository."""
        if not self._items:
            raise EmptyRepositoryError()
        return self._items[-1]

    def filter(self, predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """Filter items by a predicate function."""
        return [item for item in self._items if predicate(item)]

    def clear(self) -> None:
        """Clear all items from the repository."""
        self._items.clear()

    def delete(self, id_: str) -> None:
        """Delete an item from the repository by its ID."""
        for i, item in enumerate(self._items):
            if 'id' in item and item['id'] == id_:
                self._items.pop(i)
                return
        raise ItemNotFoundError(id_)


@pytest.fixture
def mock_repository():
    """
    Fixture that provides a mock repository instance for testing.

    The MockRepository class is defined within the fixture to keep it
    private to the fixture and hidden from other code.

    Returns:
        An instance of a mock repository implementing RepositoryInterface
    """

    return MockRepository()


@pytest.fixture(autouse=True, scope="function")
def reset_history_after_test():
    """Reset the repository singleton after each test."""
    yield  # Run the test
    MemoryRepository.reset_instance()
    CalculationHistory.reset_instance()
