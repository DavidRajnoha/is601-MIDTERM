"""CSV file repository implementation using pandas."""
import logging
import os
import pandas as pd
from typing import List, Callable, Dict, Any

from src.core.logging_decorator import log_class
from src.core.singleton import singleton
from src.persistance.repository_interface import RepositoryInterface
from src.exceptions.repository_exceptions import (
    ItemNotFoundError,
    EmptyRepositoryError,
    RepositoryIOError
)


@singleton
@log_class
class CSVRepository(RepositoryInterface[Dict[str, Any]]):
    """
    CSV file implementation of the repository interface using pandas.
    Stores and retrieves dictionaries from a CSV file.

    Implements EAFP (Easier to Ask for Forgiveness than Permission) pattern by
    raising exceptions rather than returning None or False values.
    """

    def __init__(self, file_path: str = "data/calculations.csv"):
        """
        Initialize a CSV repository.

        Args:
            file_path: Path to the CSV file where data will be stored

        Raises:
            RepositoryIOError: If there's an error creating directories or reading the file
        """
        self.file_path = file_path

        try:
            self._ensure_directory_exists()

            # Initialize the dataframe or load existing data
            if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
                try:
                    self.logger.debug("Loading CSV repository from file")
                    self._df = pd.read_csv(self.file_path)
                except Exception as e:
                    # If there's an error reading the file, start with empty dataframe
                    self.logger.error(f"Error loading CSV repository: {e}")
                    self._df = pd.DataFrame()
            else:
                self._df = pd.DataFrame()

        except Exception as e:
            raise RepositoryIOError("initialization", e)

    def _ensure_directory_exists(self) -> None:
        """
        Ensure the directory for the CSV file exists.

        Raises:
            RepositoryIOError: If there's an error creating the directory
        """
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            self.logger.debug(f"Creating directory: {directory}")
            try:
                os.makedirs(directory)
            except Exception as e:
                raise RepositoryIOError(f"creating directory {directory}", e)

    def _save_to_csv(self) -> None:
        """
        Save the current dataframe to CSV file.

        Raises:
            RepositoryIOError: If there's an error saving to the file
        """
        self.logger.debug("Saving CSV repository to file")
        try:
            self._df.to_csv(self.file_path, index=False)
        except Exception as e:
            raise RepositoryIOError("saving to CSV", e)

    def add(self, item: Dict[str, Any]) -> None:
        """
        Add an item dictionary to the repository.

        Args:
            item: The dictionary to add

        Raises:
            RepositoryIOError: If there's an error adding the item or saving to CSV
        """
        try:
            new_row = pd.DataFrame([item])
            self._df = pd.concat([self._df, new_row], ignore_index=True)
            self.logger.debug(f"Added item to CSV repository: {item}")

            self._save_to_csv()
        except Exception as e:
            raise RepositoryIOError("adding item", e)

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all items from the repository.

        Returns:
            A list of all dictionaries in the repository

        Raises:
            EmptyRepositoryError: If the repository is empty
        """
        if self._df.empty:
            raise EmptyRepositoryError()

        return [row.to_dict() for _, row in self._df.iterrows()]

    def get_by_id(self, id: str) -> Dict[str, Any]:
        """
        Get an item by its ID.

        Args:
            id: The ID of the item to retrieve

        Returns:
            The dictionary if found

        Raises:
            ItemNotFoundError: If no item with the given ID exists
        """
        if self._df.empty:
            raise ItemNotFoundError(id)

        filtered = self._df[self._df['id'] == id]
        if filtered.empty:
            raise ItemNotFoundError(id)

        return filtered.iloc[0].to_dict()

    def get_last(self) -> Dict[str, Any]:
        """
        Get the last item added to the repository.

        Returns:
            The last dictionary

        Raises:
            EmptyRepositoryError: If the repository is empty
        """
        if self._df.empty:
            raise EmptyRepositoryError()

        return self._df.iloc[-1].to_dict()

    def filter(self, predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """
        Filter items by a predicate function.

        Args:
            predicate: A function that takes a dictionary and returns a boolean

        Returns:
            A list of dictionaries for which the predicate returns True
        """
        # Filter returns an empty list if no matches instead of raising an exception
        # since an empty result is a valid outcome for filtering
        if self._df.empty:
            return []

        all_items = [row.to_dict() for _, row in self._df.iterrows()]
        return [item for item in all_items if predicate(item)]

    def clear(self) -> None:
        """
        Clear all items from the repository.

        Raises:
            RepositoryIOError: If there's an error clearing the repository or saving to CSV
        """
        try:
            self.logger.debug("Clearing CSV repository")
            self._df = pd.DataFrame()
            self._save_to_csv()
        except Exception as e:
            raise RepositoryIOError("clearing repository", e)

    def delete(self, id: str) -> None:
        """Delete an item from the repository by its ID."""
        initial_len = len(self._df)
        self._df = self._df[self._df['id'] != id]

        if len(self._df) == initial_len:
            # No rows were deleted, item wasn't found
            raise ItemNotFoundError(id)

        try:
            self._save_to_csv()
        except Exception as e:
            raise RepositoryIOError(f"saving after deleting item with ID {id}", e)