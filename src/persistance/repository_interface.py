"""Generic repository interface definition."""
from typing import Generic, TypeVar, List, Optional, Callable, Dict, Any

# Use Dict[str, Any] as the base type for all repositories
# This makes repositories store generic dictionaries rather than specific objects
T = TypeVar('T')


class RepositoryInterface(Generic[T]):
    """
    Interface for all repository implementations.

    Repositories store and retrieve items as dictionaries,
    with no knowledge of the specific object types they represent.
    """

    def add(self, item: T) -> None:
        """
        Add an item to the repository.

        Args:
            item: The item to add
        """
        pass

    def get_all(self) -> List[T]:
        """
        Get all items from the repository.

        Returns:
            A list of all items in the repository
        """
        pass

    def get_by_id(self, id: str) -> Optional[T]:
        """
        Get an item by its ID.

        Args:
            id: The ID of the item to retrieve

        Returns:
            The item if found, None otherwise
        """
        pass

    def get_last(self) -> Optional[T]:
        """
        Get the last item added to the repository.

        Returns:
            The last item if repository is not empty, None otherwise
        """
        pass

    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        Filter items by a predicate function.

        Args:
            predicate: A function that takes an item and returns a boolean

        Returns:
            A list of items for which the predicate returns True
        """
        pass

    def clear(self) -> None:
        """Clear all items from the repository."""
        pass

    def delete(self, id: str) -> bool:
        """
        Delete an item from the repository by its ID.

        Args:
            id: The ID of the item to delete

        Returns:
            bool: True if item was found and deleted, False otherwise
        """
        pass