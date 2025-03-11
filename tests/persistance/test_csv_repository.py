"""Tests for the CSVRepository class."""
# pylint: disable=redefined-outer-name, no-member, duplicate-code
# code duplication in test is ok for readability
import os
import shutil
from datetime import datetime
import pytest

from src.persistance.csv_repository import CSVRepository


@pytest.fixture(autouse=True, scope="function")
def reset_history_after_test():
    """Reset the repository singleton after each test."""
    yield
    CSVRepository.reset_instance()


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
def test_items():
    """Create test dictionary items."""
    return [
        {
            'id': "1",
            'operation_name': "add",
            'operands': "10,5",
            'result': "15",
            'timestamp': datetime.now().isoformat()
        },
        {
            'id': "2",
            'operation_name': "subtract",
            'operands': "20,8",
            'result': "12",
            'timestamp': datetime.now().isoformat()
        },
        {
            'id': "3",
            'operation_name': "multiply",
            'operands': "6,7",
            'result': "42",
            'timestamp': datetime.now().isoformat()
        }
    ]


@pytest.fixture
def populated_repository(test_items, csv_file_path):
    """Create a repository pre-populated with test items."""
    # Make sure we start with a clean state
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    repository = CSVRepository(file_path=csv_file_path)
    for item in test_items:
        repository.add(item)
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


def test_add(empty_repository, test_items):
    """Test adding items to the repository."""
    empty_repository.add(test_items[0])

    all_items = empty_repository.get_all()
    assert len(all_items) == 1

    item = all_items[0]
    assert item['id'] == test_items[0]['id']
    assert item['operation_name'] == test_items[0]['operation_name']
    assert item['result'] == test_items[0]['result']


def test_get_all(populated_repository, test_items):
    """Test getting all items from the repository."""
    all_items = populated_repository.get_all()
    assert len(all_items) == len(test_items)

    results = [item['result'] for item in all_items]
    expected_results = [item['result'] for item in test_items]
    for result in expected_results:
        assert result in results


def test_get_by_id(populated_repository, test_items):
    """Test getting an item by ID."""
    item = populated_repository.get_by_id("2")
    assert item is not None
    assert item['id'] == "2"
    assert item['result'] == test_items[1]['result']


def test_get_by_id_not_found(populated_repository):
    """Test getting an item by ID when the ID doesn't exist."""
    item = populated_repository.get_by_id("999")
    assert item is None


def test_get_last(populated_repository, test_items):
    """Test getting the last item in the repository."""
    last_item = populated_repository.get_last()
    assert last_item is not None
    assert last_item['id'] == "3"  # The last test item
    assert last_item['result'] == test_items[2]['result']


def test_get_last_empty_repository(empty_repository):
    """Test getting the last item from an empty repository."""
    assert empty_repository.get_last() is None


def test_filter(populated_repository):
    """Test filtering items by a predicate."""
    # Filter items where result > 20 (as string comparison)
    filtered_items = populated_repository.filter(
        lambda item: int(item['result']) > 20
    )
    assert len(filtered_items) == 1
    assert filtered_items[0]['result'] == "42"


def test_clear(populated_repository):
    """Test clearing the repository."""
    assert len(populated_repository.get_all()) == 3
    populated_repository.clear()
    assert len(populated_repository.get_all()) == 0
    assert populated_repository.get_last() is None


def test_persistence(csv_file_path, test_items):
    """Test that repository persists data between instances."""
    repo1 = CSVRepository(file_path=csv_file_path)
    for item in test_items:
        repo1.add(item)

    repo2 = CSVRepository(file_path=csv_file_path)

    assert len(repo2.get_all()) == len(test_items)

    new_item = {
        'id': "4",
        'operation_name': "divide",
        'operands': "10,2",
        'result': "5",
        'timestamp': datetime.now().isoformat()
    }
    repo2.add(new_item)

    repo3 = CSVRepository(file_path=csv_file_path)
    assert len(repo3.get_all()) == len(test_items) + 1


def test_delete(populated_repository):
    """Test deleting a specific item from the repository."""
    initial_item_count = len(populated_repository.get_all())
    delete_result = populated_repository.delete("2")
    remaining_items = populated_repository.get_all()

    assert delete_result is True
    assert len(remaining_items) == initial_item_count - 1
    assert all(item['id'] != "2" for item in remaining_items)
    assert any(item['id'] == "1" for item in remaining_items)
    assert any(item['id'] == "3" for item in remaining_items)


def test_delete_nonexistent(populated_repository):
    """Test deleting an item that doesn't exist."""
    initial_item_count = len(populated_repository.get_all())
    delete_result = populated_repository.delete("999")

    assert delete_result is False
    assert len(populated_repository.get_all()) == initial_item_count
