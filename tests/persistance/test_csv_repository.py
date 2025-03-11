"""Tests for the CSVRepository class."""
# pylint: disable=redefined-outer-name, no-member, duplicate-code
# code duplication in test is ok for readability
import os
import shutil
from decimal import Decimal
from datetime import datetime
import pytest
import pandas as pd

from src.persistance.csv_repository import CSVRepository
from src.model.calculation import Calculation
from src.operations import basic
from src.core.operation_registry import operation_registry


@pytest.fixture(autouse=True, scope="function")
def reset_history_after_test():
    """Reset the repository singleton after each test."""
    yield
    CSVRepository.reset_instance()

class MockCalculation:
    """
    Mock class to patch the Calculation class for testing.
    """

    @staticmethod
    def to_dict(calculation):
        """Static method to convert a Calculation to a dictionary."""
        return {
            'id': calculation.id,
            'operation_name': calculation.operation_name,
            'operands': ','.join(str(op) for op in calculation.operands),
            'result': str(calculation.result) if calculation.result is not None else '',
            'timestamp': calculation.timestamp.isoformat()
            if hasattr(calculation, 'timestamp') else datetime.now().isoformat()
        }

    @staticmethod
    def from_dict(data):
        """Static method to create a Calculation from a dictionary."""
        if isinstance(data, pd.Series):
            data = data.to_dict()

        # Get the operation function from the registry
        operation_name = data['operation_name']
        operation = operation_registry.get(operation_name)

        operands = [Decimal(op) for op in data['operands'].split(',')]

        calculation = Calculation(operation, *operands)
        calculation.id = data['id']
        calculation.result = Decimal(data['result']) if data['result'] else None

        if 'timestamp' in data and data['timestamp']:
            try:
                calculation.timestamp = datetime.fromisoformat(data['timestamp'])
            except (ValueError, TypeError):
                calculation.timestamp = datetime.now()

        return calculation


@pytest.fixture(autouse=True)
def patch_calculation(monkeypatch):
    """Patch Calculation.to_dict and Calculation.from_dict for testing."""
    monkeypatch.setattr(Calculation, 'to_dict', MockCalculation.to_dict)
    monkeypatch.setattr(Calculation, 'from_dict', MockCalculation.from_dict)


@pytest.fixture
def test_data_dir():
    """Create a temporary directory for test data."""
    test_dir = "test_data"
    os.makedirs(test_dir, exist_ok=True)
    yield test_dir
    shutil.rmtree(test_dir)


@pytest.fixture
def csv_file_path(test_data_dir):
    """Create a path to a test CSV file."""
    return os.path.join(test_data_dir, "test_repository.csv")


@pytest.fixture
def test_calculations():
    """Create test calculation objects."""
    calculations = []

    calc1 = Calculation(basic.add, Decimal('10'), Decimal('5'))
    calc1.id = "1"
    calc1.result = Decimal('15')
    calc1.timestamp = datetime.now()
    calculations.append(calc1)

    calc2 = Calculation(basic.subtract, Decimal('20'), Decimal('8'))
    calc2.id = "2"
    calc2.result = Decimal('12')
    calc2.timestamp = datetime.now()
    calculations.append(calc2)

    calc3 = Calculation(basic.multiply, Decimal('6'), Decimal('7'))
    calc3.id = "3"
    calc3.result = Decimal('42')
    calc3.timestamp = datetime.now()
    calculations.append(calc3)

    return calculations


@pytest.fixture
def populated_repository(test_calculations, csv_file_path):
    """Create a repository pre-populated with test calculations."""
    # Make sure we start with a clean state
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    repository = CSVRepository(file_path=csv_file_path)
    for calc in test_calculations:
        repository.add(calc)
    return repository


@pytest.fixture
def empty_repository(csv_file_path):
    """Create an empty repository for testing."""
    # Make sure we start with a clean state
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    return CSVRepository(file_path=csv_file_path)


def test_initialization(csv_file_path):
    """Test repository initialization and file creation."""
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    CSVRepository(file_path=csv_file_path)

    assert os.path.exists(os.path.dirname(csv_file_path))


def test_add(empty_repository, test_calculations):
    """Test adding items to the repository."""
    empty_repository.add(test_calculations[0])

    all_items = empty_repository.get_all()
    assert len(all_items) == 1

    item = all_items[0]
    assert item.id == test_calculations[0].id
    assert item.operation_name == test_calculations[0].operation_name
    assert item.result == test_calculations[0].result


def test_get_all(populated_repository, test_calculations):
    """Test getting all items from the repository."""
    all_items = populated_repository.get_all()
    assert len(all_items) == len(test_calculations)

    results = [item.result for item in all_items]
    expected_results = [calc.result for calc in test_calculations]
    for result in expected_results:
        assert result in results


def test_get_by_id(populated_repository, test_calculations):
    """Test getting an item by ID."""
    item = populated_repository.get_by_id("2")
    assert item is not None
    assert item.id == "2"
    assert item.result == test_calculations[1].result


def test_get_by_id_not_found(populated_repository):
    """Test getting an item by ID when the ID doesn't exist."""
    item = populated_repository.get_by_id("999")
    assert item is None


def test_get_last(populated_repository, test_calculations):
    """Test getting the last item in the repository."""
    last_item = populated_repository.get_last()
    assert last_item is not None
    assert last_item.id == "3"  # The last test calculation
    assert last_item.result == test_calculations[2].result


def test_get_last_empty_repository(empty_repository):
    """Test getting the last item from an empty repository."""
    assert empty_repository.get_last() is None


def test_filter(populated_repository):
    """Test filtering items by a predicate."""
    # Filter items where result > 20
    filtered_items = populated_repository.filter(
        lambda calc: calc.result > Decimal('20')
    )
    assert len(filtered_items) == 1
    assert filtered_items[0].result == Decimal('42')


def test_clear(populated_repository):
    """Test clearing the repository."""
    assert len(populated_repository.get_all()) == 3
    populated_repository.clear()
    assert len(populated_repository.get_all()) == 0
    assert populated_repository.get_last() is None


def test_persistence(csv_file_path, test_calculations):
    """Test that repository persists data between instances."""
    repo1 = CSVRepository(file_path=csv_file_path)
    for calc in test_calculations:
        repo1.add(calc)

    repo2 = CSVRepository(file_path=csv_file_path)

    assert len(repo2.get_all()) == len(test_calculations)

    new_calc = Calculation(basic.divide,Decimal('10'), Decimal('2'))
    new_calc.id = "4"
    new_calc.result = Decimal('5')
    new_calc.timestamp = datetime.now()
    repo2.add(new_calc)

    repo3 = CSVRepository(file_path=csv_file_path)
    assert len(repo3.get_all()) == len(test_calculations) + 1


def test_delete(populated_repository):
    """Test deleting a specific calculation from the repository."""
    initial_calculation_count = len(populated_repository.get_all())
    delete_result = populated_repository.delete("2")
    remaining_calculations = populated_repository.get_all()

    assert delete_result is True
    assert len(remaining_calculations) == initial_calculation_count - 1
    assert all(calc.id != "2" for calc in remaining_calculations)
    assert any(calc.id == "1" for calc in remaining_calculations)
    assert any(calc.id == "3" for calc in remaining_calculations)


def test_delete_nonexistent(populated_repository):
    """Test deleting a calculation that doesn't exist."""
    initial_calculation_count = len(populated_repository.get_all())
    delete_result = populated_repository.delete("999")

    assert delete_result is False
    assert len(populated_repository.get_all()) == initial_calculation_count
