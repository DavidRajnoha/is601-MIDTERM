"""Tests for the CalculationHistory class."""
from decimal import Decimal
from typing import List, Callable, Dict, Any

import pytest  # pylint: disable=wrong-import-order

from src.model.calculation import Calculation
from src.persistance.calculation_history import CalculationHistory
from src.persistance.memory_repository import MemoryRepository
from src.operations.basic import add, subtract, multiply


# Fixtures for common testing needs

@pytest.fixture
def history() -> CalculationHistory:
    """Create a new calculation history with an empty repository."""
    repository = MemoryRepository[Calculation]()
    return CalculationHistory(repository)


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
def standard_calculations(create_calculation, history) -> Dict[str, Calculation]:  # pylint: disable=redefined-outer-name
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
def calculations_by_operation(create_calculation, history) -> List[Calculation]:  # pylint: disable=redefined-outer-name
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
def calculations_by_result(create_calculation, history) -> List[Calculation]:  # pylint: disable=redefined-outer-name
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


# Tests
def test_add_calculation(history, executed_calculation):  # pylint: disable=redefined-outer-name
    """Test adding a calculation to the history."""
    # Add calculation to history
    history.add_calculation(executed_calculation)

    # Verify it's in the history
    assert len(history.get_all_calculations()) == 1
    assert history.get_last_calculation() == executed_calculation


def test_get_all_calculations(history, standard_calculations):  # pylint: disable=redefined-outer-name
    """Test getting all calculations from history."""
    # Verify standard_calculations were properly added to history
    assert len(standard_calculations) == 3  # Use standard_calculations to satisfy pylint
    calculations = history.get_all_calculations()
    assert len(calculations) == 3
    assert calculations[0].result == Decimal('3')  # 1 + 2
    assert calculations[1].result == Decimal('6')  # 10 - 4
    assert calculations[2].result == Decimal('9')  # 3 * 3


def test_get_calculation_by_id(history, standard_calculations):  # pylint: disable=redefined-outer-name
    """Test retrieving a calculation by its ID."""
    # Get the ID of the subtraction calculation
    target_id = standard_calculations["subtract_10_4"].id

    # Retrieve by ID
    retrieved_calc = history.get_calculation_by_id(target_id)
    assert retrieved_calc is not None
    assert retrieved_calc.id == target_id
    assert retrieved_calc.result == Decimal('6')  # 10 - 4


def test_get_calculation_by_id_not_found(history, executed_calculation):  # pylint: disable=redefined-outer-name
    """Test retrieving a calculation with a non-existent ID."""
    history.add_calculation(executed_calculation)
    retrieved_calc = history.get_calculation_by_id("non-existent-id")
    assert retrieved_calc is None


def test_get_last_calculation(history, standard_calculations):  # pylint: disable=redefined-outer-name
    """Test getting the most recent calculation."""
    retrieved_last = history.get_last_calculation()
    assert retrieved_last is not None
    assert retrieved_last.id == standard_calculations["multiply_3_3"].id
    assert retrieved_last.result == Decimal('9')  # 3 * 3


def test_get_last_calculation_empty_history(history):  # pylint: disable=redefined-outer-name
    """Test getting the last calculation from an empty history."""
    assert history.get_last_calculation() is None


def test_filter_calculations_by_operation(history, calculations_by_operation):  # pylint: disable=redefined-outer-name
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


def test_filter_calculations_by_result(history, calculations_by_result):  # pylint: disable=redefined-outer-name
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


def test_clear_history(history, create_calculation):  # pylint: disable=redefined-outer-name
    """Test clearing all calculation history."""
    # Add some calculations
    history.add_calculation(create_calculation(add, 1, 2))
    history.add_calculation(create_calculation(subtract, 10, 4))

    assert len(history.get_all_calculations()) == 2

    # Clear history
    history.clear_history()
    assert len(history.get_all_calculations()) == 0
    assert history.get_last_calculation() is None
