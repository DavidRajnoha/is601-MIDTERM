"""Tests for the Calculation class."""
from decimal import Decimal
from functools import reduce
import pytest

from src.model.calculation import Calculation
from src.operations.basic import add, subtract, multiply, divide


def multi_add(*args) -> Decimal:
    """Add multiple operands together."""
    return Decimal(sum(args))


def multi_multiply(*args) -> Decimal:
    """Multiply multiple operands together."""
    return reduce(lambda x, y: x * y, args)


def multi_subtract(*args) -> Decimal:
    """Subtract all operands from the first one."""
    if len(args) <= 1:
        return args[0]
    return args[0] - sum(args[1:])


def multi_divide(*args) -> Decimal:
    """Divide the first operand by the product of the rest."""
    if len(args) <= 1:
        return args[0]
    return args[0] / reduce(lambda x, y: x * y, args[1:])


class TestCalculation:
    """Test cases for the Calculation class."""

    def test_calculation_with_two_operands(self):
        """Test calculation with traditional two operands."""
        # Test with binary operations
        calc = Calculation(add, Decimal('5'), Decimal('3'))
        assert calc.perform_operation() == Decimal('8')

        calc = Calculation(subtract, Decimal('5'), Decimal('3'))
        assert calc.perform_operation() == Decimal('2')

        calc = Calculation(multiply, Decimal('5'), Decimal('3'))
        assert calc.perform_operation() == Decimal('15')

        calc = Calculation(divide, Decimal('6'), Decimal('3'))
        assert calc.perform_operation() == Decimal('2')

    def test_calculation_with_multiple_operands(self):
        """Test calculation with multiple operands."""
        # Test with multi-operand operations
        calc = Calculation(multi_add, Decimal('5'), Decimal('3'), Decimal('2'), Decimal('1'))
        assert calc.perform_operation() == Decimal('11')  # 5 + 3 + 2 + 1 = 11

        calc = Calculation(multi_multiply, Decimal('2'), Decimal('3'), Decimal('4'))
        assert calc.perform_operation() == Decimal('24')  # 2 * 3 * 4 = 24

        calc = Calculation(multi_subtract, Decimal('10'), Decimal('2'), Decimal('3'))
        assert calc.perform_operation() == Decimal('5')  # 10 - (2 + 3) = 5

        calc = Calculation(multi_divide, Decimal('24'), Decimal('2'), Decimal('3'))
        assert calc.perform_operation() == Decimal('4')  # 24 / (2 * 3) = 4

    def test_calculation_with_different_input_types(self):
        """Test calculation with different input types that convert to Decimal."""
        calc = Calculation(multi_add, 5, 3.5, "2.5")
        assert calc.perform_operation() == Decimal('11')

        calc = Calculation(multi_multiply, 2, "3", 4.5)
        assert calc.perform_operation() == Decimal('27')

    def test_calculation_with_single_operand(self):
        """Test calculation with a single operand."""
        calc = Calculation(multi_add, Decimal('5'))
        assert calc.perform_operation() == Decimal('5')

    def test_calculation_with_zero_operands(self):
        """Test calculation with no operands raises ValueError."""
        with pytest.raises(ValueError):
            Calculation(multi_add)

    def test_division_by_zero(self):
        """Test division by zero raises ZeroDivisionError."""
        calc = Calculation(divide, Decimal('10'), Decimal('0'))
        with pytest.raises(ZeroDivisionError):
            calc.perform_operation()

    def test_type_errors_are_propagated(self):
        """Test that TypeError is propagated when operation has wrong signature."""
        def binary_only(num1, num2):
            return num1 + num2

        calc = Calculation(binary_only, Decimal('1'), Decimal('2'), Decimal('3'))
        with pytest.raises(TypeError):
            calc.perform_operation()
