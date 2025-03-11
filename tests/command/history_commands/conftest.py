"""Fixtures for testing history commands."""
from decimal import Decimal

from unittest.mock import MagicMock
import pytest

from src.model.calculation import Calculation

@pytest.fixture
def mock_calculations(add_operation, divide_operation):
    """Create mock calculation objects for testing."""
    calc1 = Calculation(add_operation, Decimal("5"), Decimal("3"), Decimal("8"))
    calc1.id = "calc1"

    calc2 = Calculation(divide_operation, Decimal("10"), Decimal("4"))
    calc2.id = "calc2"

    return [calc1, calc2]

@pytest.fixture
def mock_history():
    """Create a mock calculation history for testing."""
    mock = MagicMock()

    mock.get_all_calculations.return_value = []
    mock.get_calculation_by_id.return_value = None
    mock.delete_calculation.return_value = False
    return mock
