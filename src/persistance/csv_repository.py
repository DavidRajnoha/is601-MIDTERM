import logging
import os
import pandas as pd
from typing import List, Optional, Callable

from src.core.logging import log_class
from src.core.singleton import singleton
from src.model.calculation import Calculation
from src.persistance.repository_interface import RepositoryInterface, T


@singleton
@log_class
class CSVRepository(RepositoryInterface[Calculation]):
    """
    CSV file implementation of the repository interface using pandas.
    Stores and retrieves items from a CSV file.
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



    def add(self, item: T) -> None:
        """
        Add an item to the repository.

        Args:
            item: The item to add
        """
        item_dict = Calculation.to_dict(item)

        new_row = pd.DataFrame([item_dict])
        self._df = pd.concat([self._df, new_row], ignore_index=True)
        logging.debug(f"Added item to CSV repository: {item}")

        self._save_to_csv()

    def get_all(self) -> List[Calculation]:
        """
        Get all items from the repository.

        Returns:
            A list of all items in the repository
        """
        if self._df.empty:
            return []

        return [Calculation.from_dict(row.to_dict()) for _, row in self._df.iterrows()]

    def get_by_id(self, id: str) -> Optional[Calculation]:
        """
        Get an item by its ID.

        Args:
            id: The ID of the item to retrieve

        Returns:
            The item if found, None otherwise
        """
        if self._df.empty:
            return None

        filtered = self._df[self._df['id'] == id]
        if filtered.empty:
            return None

        return Calculation.from_dict(filtered.iloc[0])

    def get_last(self) -> Optional[T]:
        """
        Get the last item added to the repository.

        Returns:
            The last item if repository is not empty, None otherwise
        """
        if self._df.empty:
            return None

        return Calculation.from_dict(self._df.iloc[-1])

    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        Filter items by a predicate function.

        Args:
            predicate: A function that takes an item and returns a boolean

        Returns:
            A list of items for which the predicate returns True
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