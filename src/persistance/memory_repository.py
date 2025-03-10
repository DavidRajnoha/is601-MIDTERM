from typing import List, Optional, Callable

from src.core.logging import log_method, log_class
from src.core.singleton import singleton
from src.model.calculation import Calculation
from src.persistance.repository_interface import RepositoryInterface, T

@singleton
@log_class
class MemoryRepository(RepositoryInterface[Calculation]):
    # TODO: Change the singleton to work with generic types
    """In-memory implementation of the repository interface."""
    
    def __init__(self):
        """Initialize an empty repository."""
        self._items: List[T] = []

    def add(self, item: T) -> None:
        """
        Add an item to the repository.
        
        Args:
            item: The item to add
        """
        self._items.append(item)

    def get_all(self) -> List[T]:
        """
        Get all items from the repository.
        
        Returns:
            A list of all items in the repository
        """
        return self._items.copy()

    def get_by_id(self, id: str) -> Optional[T]:
        """
        Get an item by its ID.
        
        Args:
            id: The ID of the item to retrieve
            
        Returns:
            The item if found, None otherwise
        """
        for item in self._items:
            if hasattr(item, 'id') and getattr(item, 'id') == id:
                return item
        return None

    def get_last(self) -> Optional[T]:
        """
        Get the last item added to the repository.
        
        Returns:
            The last item if repository is not empty, None otherwise
        """
        if not self._items:
            return None
        return self._items[-1]

    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        Filter items by a predicate function.
        
        Args:
            predicate: A function that takes an item and returns a boolean
            
        Returns:
            A list of items for which the predicate returns True
        """
        return [item for item in self._items if predicate(item)]

    def clear(self) -> None:
        """Clear all items from the repository."""
        self._items.clear()
