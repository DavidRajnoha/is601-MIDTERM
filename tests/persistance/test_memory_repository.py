"""Tests for the MemoryRepository class."""
# code duplication in test is ok for readability
from dataclasses import dataclass
from typing import List

import pytest

from src.persistance.memory_repository import MemoryRepository


@dataclass
class MockItem:
    """Simple test item class for repository testing."""
    id: str
    name: str
    value: int


@pytest.fixture
def test_items() -> List[MockItem]:
    """Create a list of test items for repository testing."""
    return [
        MockItem(id="1", name="Item 1", value=10),
        MockItem(id="2", name="Item 2", value=20),
        MockItem(id="3", name="Item 3", value=30)
    ]


@pytest.fixture
def populated_repository(test_items) -> MemoryRepository:  # pylint: disable=redefined-outer-name
    """Create a repository pre-populated with test items."""
    repository = MemoryRepository()
    for item in test_items:
        repository.add(item)
    return repository


@pytest.fixture
def empty_repository() -> MemoryRepository:
    """Create an empty repository for testing."""
    return MemoryRepository()


def test_add(populated_repository):  # pylint: disable=redefined-outer-name
    """Test adding items to the repository."""
    new_item = MockItem(id="4", name="Item 4", value=40)
    populated_repository.add(new_item)
    assert len(populated_repository.get_all()) == 4
    assert populated_repository.get_by_id("4") == new_item


def test_get_all(populated_repository):  # pylint: disable=redefined-outer-name
    """Test getting all items from the repository."""
    all_items = populated_repository.get_all()
    assert len(all_items) == 3
    # Make sure get_all returns a copy of the items
    all_items.append(MockItem(id="4", name="Item 4", value=40))
    assert len(populated_repository.get_all()) == 3


def test_get_by_id(populated_repository):  # pylint: disable=redefined-outer-name
    """Test getting an item by ID."""
    item = populated_repository.get_by_id("2")
    assert item is not None
    assert item.id == "2"
    assert item.name == "Item 2"
    assert item.value == 20


def test_get_by_id_not_found(populated_repository):  # pylint: disable=redefined-outer-name
    """Test getting an item by ID when the ID doesn't exist."""
    item = populated_repository.get_by_id("999")
    assert item is None


def test_get_last(populated_repository):  # pylint: disable=redefined-outer-name
    """Test getting the last item in the repository."""
    last_item = populated_repository.get_last()
    assert last_item is not None
    assert last_item.id == "3"


def test_get_last_empty_repository(empty_repository):  # pylint: disable=redefined-outer-name
    """Test getting the last item from an empty repository."""
    assert empty_repository.get_last() is None


def test_filter(populated_repository):  # pylint: disable=redefined-outer-name
    """Test filtering items by a predicate."""
    filtered_items = populated_repository.filter(lambda item: item.value > 15)
    assert len(filtered_items) == 2
    assert filtered_items[0].id == "2"
    assert filtered_items[1].id == "3"


def test_clear(populated_repository):  # pylint: disable=redefined-outer-name
    """Test clearing the repository."""
    assert len(populated_repository.get_all()) == 3
    populated_repository.clear()
    assert len(populated_repository.get_all()) == 0
    assert populated_repository.get_last() is None


def test_delete(populated_repository):  # pylint: disable=redefined-outer-name
    """Test deleting a specific item from the repository."""
    initial_item_count = len(populated_repository.get_all())
    delete_result = populated_repository.delete("2")
    remaining_items = populated_repository.get_all()

    assert delete_result is True
    assert len(remaining_items) == initial_item_count - 1
    assert all(item.id != "2" for item in remaining_items)
    assert any(item.id == "1" for item in remaining_items)
    assert any(item.id == "3" for item in remaining_items)


def test_delete_nonexistent(populated_repository):  # pylint: disable=redefined-outer-name
    """Test deleting an item that doesn't exist."""
    initial_item_count = len(populated_repository.get_all())
    delete_result = populated_repository.delete("999")

    assert delete_result is False
    assert len(populated_repository.get_all()) == initial_item_count
