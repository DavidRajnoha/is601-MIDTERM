"""In-memory repository implementation."""
from typing import List, Optional, Callable, Dict, Any

from src.core.logging import log_method, log_class
from src.core.singleton import singleton
from src.persistance.repository_interface import RepositoryInterface


@singleton
@log_class
class MemoryRepository(RepositoryInterface[Dict[str, Any]]):
    """
    In-memory implementation of the repository interface.
    Stores dictionaries in a list, with no knowledge of specific object types.
    """

    def __init__(self):
        """Initialize an empty repository."""
        self._items: List[Dict[str, Any]] = []

    def add(self, item: Dict[str, Any]) -> None:
        """
        Add an item to the repository.

        Args:
            item: The dictionary to add
        """
        self._items.append(item)

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all items from the repository.

        Returns:
            A list of all items in the repository
        """
        return self._items.copy()

    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get an item by its ID.

        Args:
            id: The ID of the item to retrieve

        Returns:
            The item if found, None otherwise
        """
        for item in self._items:
            if 'id' in item and item['id'] == id:
                return item
        return None

    def get_last(self) -> Optional[Dict[str, Any]]:
        """
        Get the last item added to the repository.

        Returns:
            The last item if repository is not empty, None otherwise
        """
        if not self._items:
            return None
        return self._items[-1]

    def filter(self, predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """
        Filter items by a predicate function.

        Args:
            predicate: A function that takes a dictionary and returns a boolean

        Returns:
            A list of items for which the predicate returns True
        """
        return [item for item in self._items if predicate(item)]

    def clear(self) -> None:
        """Clear all items from the repository."""
        self._items.clear()

    def delete(self, id: str) -> bool:
        """
        Delete an item from the repository by its ID.

        Args:
            id: The ID of the item to delete

        Returns:
            bool: True if item was found and deleted, False otherwise
        """
        for i, item in enumerate(self._items):
            if 'id' in item and item['id'] == id:
                self._items.pop(i)
                return True
        return False