"""In-memory repository implementation."""
import logging
from typing import List, Callable, Dict, Any

from src.core.logging_decorator import log_class
from src.core.singleton import singleton
from src.persistance.repository_interface import RepositoryInterface
from src.exceptions.repository_exceptions import (
    ItemNotFoundError,
    EmptyRepositoryError
)


@singleton
@log_class
class MemoryRepository(RepositoryInterface[Dict[str, Any]]):
    """
    In-memory implementation of the repository interface.
    Stores dictionaries in a list, with no knowledge of specific object types.

    Implements EAFP (Easier to Ask for Forgiveness than Permission) pattern by
    raising exceptions rather than returning None or False values.
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
        logging.debug(f"Added item with ID {item.get('id')} to memory repository")

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all items from the repository.

        Returns:
            A list of all items in the repository

        Raises:
            EmptyRepositoryError: If the repository is empty
        """
        if not self._items:
            raise EmptyRepositoryError()

        return self._items.copy()

    def get_by_id(self, id: str) -> Dict[str, Any]:
        """
        Get an item by its ID.

        Args:
            id: The ID of the item to retrieve

        Returns:
            The item if found

        Raises:
            ItemNotFoundError: If no item with the given ID exists
        """
        for item in self._items:
            if 'id' in item and item['id'] == id:
                return item

        raise ItemNotFoundError(id)

    def get_last(self) -> Dict[str, Any]:
        """
        Get the last item added to the repository.

        Returns:
            The last item

        Raises:
            EmptyRepositoryError: If the repository is empty
        """
        if not self._items:
            raise EmptyRepositoryError()

        return self._items[-1]

    def filter(self, predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """
        Filter items by a predicate function.

        Args:
            predicate: A function that takes a dictionary and returns a boolean

        Returns:
            A list of items for which the predicate returns True
        """
        # Filter returns an empty list if no matches instead of raising an exception
        # since an empty result is a valid outcome for filtering
        return [item for item in self._items if predicate(item)]

    def clear(self) -> None:
        """Clear all items from the repository."""
        self._items.clear()
        logging.debug("Cleared memory repository")

    def delete(self, id: str) -> None:
        """
        Delete an item from the repository by its ID.

        Args:
            id: The ID of the item to delete

        Raises:
            ItemNotFoundError: If no item with the given ID exists
        """
        for i, item in enumerate(self._items):
            if 'id' in item and item['id'] == id:
                self._items.pop(i)
                logging.debug(f"Deleted item with ID {id} from memory repository")
                return

        raise ItemNotFoundError(id)