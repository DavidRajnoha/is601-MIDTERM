"""Generic repository interface definition."""
from typing import Generic, TypeVar, List, Callable, Dict, Any

# Use Dict[str, Any] as the base type for all repositories
# This makes repositories store generic dictionaries rather than specific objects
T = TypeVar('T')


class RepositoryInterface(Generic[T]):
    """
    Interface for all repository implementations.

    Repositories store and retrieve items as dictionaries,
    with no knowledge of the specific object types they represent.

    This interface follows the EAFP (Easier to Ask for Forgiveness than Permission) pattern.
    Methods raise appropriate exceptions when operations fail, rather than returning None or False.
    """

    def add(self, item: T) -> None:
        """
        Add an item to the repository.

        Args:
            item: The item to add

        Raises:
            RepositoryIOError: If the item cannot be added due to I/O errors
        """
        pass

    def get_all(self) -> List[T]:
        """
        Get all items from the repository.

        Returns:
            A list of all items in the repository

        Raises:
            EmptyRepositoryError: If the repository is empty
            RepositoryIOError: If items cannot be retrieved due to I/O errors
        """
        pass

    def get_by_id(self, id: str) -> T:
        """
        Get an item by its ID.

        Args:
            id: The ID of the item to retrieve

        Returns:
            The item if found

        Raises:
            ItemNotFoundError: If no item with the given ID exists
            RepositoryIOError: If the item cannot be retrieved due to I/O errors
        """
        pass

    def get_last(self) -> T:
        """
        Get the last item added to the repository.

        Returns:
            The last item

        Raises:
            EmptyRepositoryError: If the repository is empty
            RepositoryIOError: If the item cannot be retrieved due to I/O errors
        """
        pass

    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        Filter items by a predicate function.

        Args:
            predicate: A function that takes an item and returns a boolean

        Returns:
            A list of items for which the predicate returns True

        Raises:
            RepositoryIOError: If items cannot be filtered due to I/O errors
        """
        pass

    def clear(self) -> None:
        """
        Clear all items from the repository.

        Raises:
            RepositoryIOError: If items cannot be cleared due to I/O errors
        """
        pass

    def delete(self, id: str) -> None:
        """
        Delete an item from the repository by its ID.

        Args:
            id: The ID of the item to delete

        Raises:
            ItemNotFoundError: If no item with the given ID exists
            RepositoryIOError: If the item cannot be deleted due to I/O errors
        """
        pass