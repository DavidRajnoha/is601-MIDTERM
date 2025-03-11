"""CSV file repository implementation using pandas."""
import logging
import os
import pandas as pd
from typing import List, Optional, Callable, Dict, Any

from src.core.logging import log_class
from src.core.singleton import singleton
from src.persistance.repository_interface import RepositoryInterface


@singleton
@log_class
class CSVRepository(RepositoryInterface[Dict[str, Any]]):
    """
    CSV file implementation of the repository interface using pandas.
    Stores and retrieves dictionaries from a CSV file.
    """

    def __init__(self, file_path: str = "data/calculations.csv"):
        """
        Initialize a CSV repository.

        Args:
            file_path: Path to the CSV file where data will be stored
        """
        self.file_path = file_path
        self._ensure_directory_exists()

        # Initialize the dataframe or load existing data
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            try:
                logging.debug("Loading CSV repository from file")
                self._df = pd.read_csv(self.file_path)
            except Exception as e:
                # If there's an error reading the file, start with empty dataframe
                logging.error(f"Error loading CSV repository: {e}")
                self._df = pd.DataFrame()
        else:
            self._df = pd.DataFrame()

    def _ensure_directory_exists(self) -> None:
        """Ensure the directory for the CSV file exists."""
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            logging.debug(f"Creating directory: {directory}")
            os.makedirs(directory)

    def _save_to_csv(self) -> None:
        """Save the current dataframe to CSV file."""
        logging.debug("Saving CSV repository to file")
        self._df.to_csv(self.file_path, index=False)

    def add(self, item: Dict[str, Any]) -> None:
        """
        Add an item dictionary to the repository.

        Args:
            item: The dictionary to add
        """
        new_row = pd.DataFrame([item])
        self._df = pd.concat([self._df, new_row], ignore_index=True)
        logging.debug(f"Added item to CSV repository: {item}")

        self._save_to_csv()

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all items from the repository.

        Returns:
            A list of all dictionaries in the repository
        """
        if self._df.empty:
            return []

        return [row.to_dict() for _, row in self._df.iterrows()]

    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get an item by its ID.

        Args:
            id: The ID of the item to retrieve

        Returns:
            The dictionary if found, None otherwise
        """
        if self._df.empty:
            return None

        filtered = self._df[self._df['id'] == id]
        if filtered.empty:
            return None

        return filtered.iloc[0].to_dict()

    def get_last(self) -> Optional[Dict[str, Any]]:
        """
        Get the last item added to the repository.

        Returns:
            The last dictionary if repository is not empty, None otherwise
        """
        if self._df.empty:
            return None

        return self._df.iloc[-1].to_dict()

    def filter(self, predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """
        Filter items by a predicate function.

        Args:
            predicate: A function that takes a dictionary and returns a boolean

        Returns:
            A list of dictionaries for which the predicate returns True
        """
        if self._df.empty:
            return []

        all_items = self.get_all()
        return [item for item in all_items if predicate(item)]

    def clear(self) -> None:
        """Clear all items from the repository."""
        logging.debug("Clearing CSV repository")
        self._df = pd.DataFrame()
        self._save_to_csv()

    def delete(self, id: str) -> bool:
        """
        Delete an item from the repository by its ID.

        Args:
            id: The ID of the item to delete

        Returns:
            bool: True if item was found and deleted, False otherwise
        """
        if self._df.empty:
            return False

        initial_len = len(self._df)
        self._df = self._df[self._df['id'] != id]

        # Check if any rows were deleted
        deleted = len(self._df) < initial_len

        if deleted:
            logging.debug(f"Deleted item with ID {id} from CSV repository")
            self._save_to_csv()

        return deleted