"""Tests for the CalculationHistory class."""
# pylint: disable=redefined-outer-name
from decimal import Decimal
from typing import List, Callable, Dict, Any, Optional
import logging

import pytest


from src.model.calculation import Calculation
from src.persistance.calculation_history import CalculationHistory
from src.operations.basic import add, subtract, multiply


class MockRepository:
    """Mock repository that can be configured to fail for testing error handling."""

    def __init__(self):
        self._items = []
        self.fail_on_get_all = False

    def add(self, item: Dict[str, Any]) -> None:
        """Add an item to the repository."""
        self._items.append(item)

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all items, with option to simulate corrupted data."""
        if self.fail_on_get_all:
            return [{"corrupted": "data"}]  # Missing required fields
        return self._items.copy()

    def get_by_id(self, id_: str) -> Optional[Dict[str, Any]]:
        """Get an item by its ID."""
        for item in self._items:
            if 'id' in item and item['id'] == id_:
                return item
        return None

    def get_last(self) -> Optional[Dict[str, Any]]:
        """Get the last item added to the repository."""
        if not self._items:
            return None
        return self._items[-1]

    def filter(self, predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """Filter items by a predicate function."""
        return [item for item in self._items if predicate(item)]

    def clear(self) -> None:
        """Clear all items from the repository."""
        self._items.clear()

    def delete(self, id_: str) -> bool:
        """Delete an item from the repository by its ID."""
        for i, item in enumerate(self._items):
            if 'id' in item and item['id'] == id_:
                self._items.pop(i)
                return True
        return False


@pytest.fixture(scope="function")
def mock_repository() -> MockRepository:
    """Create a mock repository for testing error handling."""
    return MockRepository()


@pytest.fixture(scope="function")
def history(mock_repository) -> CalculationHistory:
    """Create a new calculation history with an empty repository."""
    return CalculationHistory(repository=mock_repository)


@pytest.fixture
def executed_calculation() -> Calculation:
    """Create and execute a simple addition calculation."""
    calc = Calculation(add, Decimal('5'), Decimal('3'))
    calc.perform_operation()
    return calc


@pytest.fixture
def create_calculation():
    """Factory fixture to create and execute a calculation with given parameters."""
    def _create_calculation(
        operation: Callable[..., Decimal],
        *args: Any
    ) -> Calculation:
        args_as_decimal = [Decimal(str(arg)) for arg in args]
        calc = Calculation(operation, *args_as_decimal)
        calc.perform_operation()
        return calc
    return _create_calculation


@pytest.fixture
def standard_calculations(create_calculation, history) -> Dict[str, Calculation]:
    """Create a set of standard calculations and add them to history."""
    calculations = {
        "add_1_2": create_calculation(add, '1', '2'),      # Result: 3
        "subtract_10_4": create_calculation(subtract, 10, 4),  # Result: 6
        "multiply_3_3": create_calculation(multiply, 3, 3)    # Result: 9
    }

    for calc in calculations.values():
        history.add_calculation(calc)

    return calculations


@pytest.fixture
def calculations_by_operation(create_calculation, history) -> List[Calculation]:
    """Create calculations with different operations for filtering tests."""
    operations_data = [
        (add, '1', '2'),      # Result: 3
        (add, '3', '4'),      # Result: 7
        (subtract, 10, 4),    # Result: 6
        (multiply, 3, 3),     # Result: 9
        (add, 5, 5)           # Result: 10
    ]

    calculations = []
    for op, a, b in operations_data:
        calc = create_calculation(op, a, b)
        history.add_calculation(calc)
        calculations.append(calc)

    return calculations


@pytest.fixture
def calculations_by_result(create_calculation, history) -> List[Calculation]:
    """Create calculations with specific results for filtering tests."""
    operations_data = [
        (add, 2, 4),         # Result: 6
        (subtract, 10, 4),   # Result: 6
        (add, 5, 5),         # Result: 10
        (multiply, 2, 3)     # Result: 6
    ]

    calculations = []
    for op, a, b in operations_data:
        calc = create_calculation(op, a, b)
        history.add_calculation(calc)
        calculations.append(calc)

    return calculations


def test_add_calculation(history, executed_calculation):
    """Test adding a calculation to the history."""
    history.add_calculation(executed_calculation)

    assert len(history.get_all_calculations()) == 1

    last_calc = history.get_last_calculation()
    assert last_calc is not None
    assert last_calc.result == executed_calculation.result
    assert last_calc.operation_name == executed_calculation.operation_name


def test_get_all_calculations(history, standard_calculations):
    """Test getting all calculations from history."""
    assert len(standard_calculations) == 3
    calculations = history.get_all_calculations()
    assert len(calculations) == 3
    assert calculations[0].result == Decimal('3')  # 1 + 2
    assert calculations[1].result == Decimal('6')  # 10 - 4
    assert calculations[2].result == Decimal('9')  # 3 * 3


def test_get_all_calculations_with_corrupted_data(history, executed_calculation,
                                                  mock_repository, caplog):
    """Test getting calculations with some corrupted data."""
    # Add one valid calculation
    history.add_calculation(executed_calculation)

    # Configure repository to return corrupted data
    mock_repository.fail_on_get_all = True

    # Get calculations with logging captured
    with caplog.at_level(logging.WARNING):
        calculations = history.get_all_calculations()

    # Should only return valid calculations (none in this case)
    assert len(calculations) == 0

    # Check that warning was logged
    assert any("Skipping invalid calculation" in record.message for record in caplog.records)


def test_get_calculation_by_id(history, standard_calculations):
    """Test retrieving a calculation by its ID."""
    # Get the ID of the subtraction calculation
    target_id = standard_calculations["subtract_10_4"].id

    # Retrieve by ID
    retrieved_calc = history.get_calculation_by_id(target_id)
    assert retrieved_calc is not None
    assert retrieved_calc.id == target_id
    assert retrieved_calc.result == Decimal('6')  # 10 - 4


def test_get_calculation_by_id_not_found(history, executed_calculation):
    """Test retrieving a calculation with a non-existent ID."""
    history.add_calculation(executed_calculation)
    retrieved_calc = history.get_calculation_by_id("non-existent-id")
    assert retrieved_calc is None


def test_get_calculation_by_id_with_corrupt_data(history, executed_calculation,
                                                 monkeypatch, caplog):
    """Test retrieving a calculation by ID with corrupted data."""
    history.add_calculation(executed_calculation)

    # Mock repository's get_by_id to return corrupted data
    # pylint: disable=unused-argument
    def mock_get_by_id(self, calc_id):
        return {"corrupted": "data"}

    monkeypatch.setattr(MockRepository, "get_by_id", mock_get_by_id)

    # Try to retrieve with logging captured
    with caplog.at_level(logging.WARNING):
        result = history.get_calculation_by_id(executed_calculation.id)

    # Should return None for corrupted data
    assert result is None

    # Check that warning was logged
    assert any("Invalid calculation data" in record.message for record in caplog.records)


def test_get_last_calculation(history, standard_calculations):
    """Test getting the most recent calculation."""
    retrieved_last = history.get_last_calculation()
    assert retrieved_last is not None
    assert retrieved_last.id == standard_calculations["multiply_3_3"].id
    assert retrieved_last.result == Decimal('9')  # 3 * 3


def test_get_last_calculation_empty_history(history):
    """Test getting the last calculation from an empty history."""
    assert history.get_last_calculation() is None


def test_filter_calculations_by_operation(history, calculations_by_operation):
    """Test filtering calculations by operation name."""
    # Verify calculations_by_operation fixture was used
    assert len(calculations_by_operation) == 5  # Use calculations_by_operation to satisfy pylint
    # Filter by add operation
    add_calculations = history.filter_calculations_by_operation("add")
    assert len(add_calculations) == 3
    assert add_calculations[0].result == Decimal('3')  # 1 + 2
    assert add_calculations[1].result == Decimal('7')  # 3 + 4
    assert add_calculations[2].result == Decimal('10')  # 5 + 5

    # Filter by multiply operation
    mult_calculations = history.filter_calculations_by_operation("multiply")
    assert len(mult_calculations) == 1
    assert mult_calculations[0].result == Decimal('9')  # 3 * 3

    # Filter by non-existent operation
    empty_calculations = history.filter_calculations_by_operation("non_existent")
    assert len(empty_calculations) == 0


def test_filter_calculations_by_result(history, calculations_by_result):
    """Test filtering calculations by result value."""
    # Verify calculations_by_result fixture was used
    assert len(calculations_by_result) == 4  # Use calculations_by_result to satisfy pylint
    # Filter by result = 6
    result_six = history.filter_calculations_by_result(Decimal('6'))
    assert len(result_six) == 3

    # Verify operations that gave result 6
    operations = [calc.operation_name for calc in result_six]
    assert "add" in operations
    assert "subtract" in operations
    assert "multiply" in operations

    # Filter by result = 10
    result_ten = history.filter_calculations_by_result(Decimal('10'))
    assert len(result_ten) == 1
    assert result_ten[0].operation_name == "add"

    # Filter by non-existent result
    empty_results = history.filter_calculations_by_result(Decimal('42'))
    assert len(empty_results) == 0


def test_clear_history(history, create_calculation):
    """Test clearing all calculation history."""
    history.add_calculation(create_calculation(add, 1, 2))
    history.add_calculation(create_calculation(subtract, 10, 4))

    assert len(history.get_all_calculations()) == 2

    history.clear_history()
    assert len(history.get_all_calculations()) == 0
    assert history.get_last_calculation() is None


def test_delete_calculation(history, create_calculation):
    """Test deleting a calculation by ID."""
    calc = create_calculation(add, 1, 2)
    history.add_calculation(calc)

    assert len(history.get_all_calculations()) == 1

    result = history.delete_calculation(calc.id)

    assert result is True
    assert len(history.get_all_calculations()) == 0
