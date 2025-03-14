"""Fixtures for testing history commands."""
from unittest.mock import Mock, MagicMock
import pytest

@pytest.fixture
def mock_history():
    """Create a mock history object."""
    mock = Mock()
    # Pre-configure common behaviors
    mock.get_all_calculations = MagicMock()
    mock.delete_calculation = MagicMock()
    return mock


@pytest.fixture
def mock_calculations():
    """Create mock calculation objects for testing."""
    calc1 = Mock()
    calc1.id = "calc1"
    calc1.operation_name = "add"
    calc1.operands = [10, 5]
    calc1.result = 15

    calc2 = Mock()
    calc2.id = "calc2"
    calc2.operation_name = "subtract"
    calc2.operands = [20, 8]
    calc2.result = 12

    return [calc1, calc2]
