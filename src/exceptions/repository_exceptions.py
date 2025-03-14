"""Module containing custom exceptions for repository operations."""


class RepositoryError(Exception):
    """Base exception for repository-related errors."""
    pass


class ItemNotFoundError(RepositoryError):
    """Exception raised when an item cannot be found in the repository."""

    def __init__(self, item_id: str):
        self.item_id = item_id
        self.message = f"Item with ID {item_id} not found in repository."
        super().__init__(self.message)


class EmptyRepositoryError(RepositoryError):
    """Exception raised when trying to access an empty repository."""

    def __init__(self):
        self.message = "Repository is empty."
        super().__init__(self.message)


class RepositoryIOError(RepositoryError):
    """Exception raised when I/O operations with the repository fail."""

    def __init__(self, operation: str, error: Exception = None):
        self.operation = operation
        self.error = error
        self.message = f"Repository I/O error during {operation}: {error}"
        super().__init__(self.message)