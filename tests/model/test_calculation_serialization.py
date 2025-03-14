"""Tests for the Calculation class serialization and deserialization."""
# pylint: disable=comparison-with-callable, invalid-name
from decimal import Decimal
import uuid
from datetime import datetime
import pytest

from src.model.calculation import Calculation
from src.operations.basic import add, subtract, multiply, divide


class TestCalculationSerialization:
    """Test cases for Calculation serialization and deserialization."""

    def test_to_dict_basic(self):
        """Test basic serialization to dictionary."""
        calc = Calculation(add, Decimal('5'), Decimal('3'))
        calc.id = "test-id-123"
        calc.result = Decimal('8')

        test_time = datetime(2023, 1, 1, 12, 0, 0)
        calc.timestamp = test_time

        data = Calculation.to_dict(calc)

        assert data['id'] == "test-id-123"
        assert data['operation_name'] == "add"
        assert data['operands'] == "5,3"
        assert data['result'] == "8"
        assert data['timestamp'] == test_time.isoformat()

    def test_to_dict_with_multiple_operands(self):
        """Test serialization with multiple operands."""
        calc = Calculation(add, Decimal('1'), Decimal('2'), Decimal('3'), Decimal('4'))
        calc.result = Decimal('10')

        data = Calculation.to_dict(calc)

        assert data['operands'] == "1,2,3,4"
        assert data['operation_name'] == "add"
        assert data['result'] == "10"

    def test_to_dict_with_no_result(self):
        """Test serialization when no result is set."""
        calc = Calculation(multiply, Decimal('5'), Decimal('3'))

        data = Calculation.to_dict(calc)

        assert data['operation_name'] == "multiply"
        assert data['result'] == ""  # Empty string for None

    def test_from_dict_basic(self):
        """Test basic deserialization from dictionary."""
        data = {
            'id': "test-id-456",
            'operation_name': "add",
            'operands': "10,5",
            'result': "15",
            'timestamp': datetime(2023, 2, 1, 12, 0, 0).isoformat()
        }

        calc = Calculation.from_dict(data)

        assert calc.id == "test-id-456"
        assert calc.operation_name == "add"
        assert calc.operation == add
        assert calc.operands == [Decimal('10'), Decimal('5')]
        assert calc.result == Decimal('15')
        assert calc.timestamp == datetime(2023, 2, 1, 12, 0, 0)

    def test_from_dict_with_multiple_operands(self):
        """Test deserialization with multiple operands."""
        data = {
            'id': "test-id-789",
            'operation_name': "multiply",
            'operands': "2,3,4",
            'result': "24",
            'timestamp': datetime(2023, 3, 1, 12, 0, 0).isoformat()
        }

        calc = Calculation.from_dict(data)

        assert calc.operation == multiply
        assert calc.operands == [Decimal('2'), Decimal('3'), Decimal('4')]
        assert calc.result == Decimal('24')

    def test_from_dict_with_no_result(self):
        """Test deserialization when no result is provided."""
        data = {
            'id': "test-id-abc",
            'operation_name': "subtract",
            'operands': "10,5",
            'result': "",
            'timestamp': datetime(2023, 4, 1, 12, 0, 0).isoformat()
        }

        calc = Calculation.from_dict(data)

        assert calc.operation == subtract
        assert calc.result is None

    def test_from_dict_with_unknown_operation(self):
        """Test deserialization with an unknown operation name."""
        data = {
            'id': "test-id-def",
            'operation_name': "unknown_operation",
            'operands': "1,2",
            'result': "3",
            'timestamp': datetime(2023, 5, 1, 12, 0, 0).isoformat()
        }

        with pytest.raises(ValueError, match="Operation not found: unknown_operation"):
            Calculation.from_dict(data)

    def test_roundtrip_serialization(self):
        """Test full serialization and deserialization cycle."""
        original = Calculation(divide, Decimal('10'), Decimal('2'))
        original.id = str(uuid.uuid4())
        original.perform_operation()  # Calculate result

        data = Calculation.to_dict(original)

        restored = Calculation.from_dict(data)

        assert restored.id == original.id
        assert restored.operation_name == original.operation_name
        assert restored.operation == original.operation
        assert restored.operands == original.operands
        assert restored.result == original.result
        assert restored.timestamp == original.timestamp

    def test_from_dict_raises_error_when_missing_required_fields(self):
        """Test that from_dict raises KeyError when required fields are missing."""
        incomplete_data = {'operation_name': 'add'}  # Missing operands field

        with pytest.raises(KeyError):
            Calculation.from_dict(incomplete_data)

    def test_from_dict_raises_error_when_operands_not_valid_decimals(self):
        """Test that from_dict raises ValueError when operands can't be converted to Decimals."""
        data_with_invalid_operands = {
            'operation_name': 'add',
            'operands': 'not,valid,decimal,values',
            'result': '',
            'id': 'test-id'
        }

        with pytest.raises(ValueError):
            Calculation.from_dict(data_with_invalid_operands)

    def test_from_dict_raises_error_when_timestamp_invalid(self):
        """Test that from_dict creates a default timestamp when timestamp format is invalid."""
        data_with_invalid_timestamp = {
            'operation_name': 'add',
            'operands': '1,2',
            'result': '3',
            'id': 'test-id',
            'timestamp': 'not-a-timestamp'
        }
        with pytest.raises(ValueError):
            Calculation.from_dict(data_with_invalid_timestamp)
