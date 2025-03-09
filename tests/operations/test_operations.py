"""Tests for basic mathematical operations."""
from decimal import Decimal

import pytest

from src.operations.basic import add, subtract, multiply, divide


class TestBasicOperations:
    """Test class for basic arithmetic operations."""

    @pytest.mark.parametrize("num1, num2, expected", [
        (Decimal('5'), Decimal('3'), Decimal('8')),
        (Decimal('-2'), Decimal('3'), Decimal('1')),
        (Decimal('0'), Decimal('0'), Decimal('0')),
        (Decimal('0.1'), Decimal('0.2'), Decimal('0.3')),
    ])
    def test_add(self, num1, num2, expected):
        """Test addition operation with various inputs."""
        assert add(num1, num2) == expected

    @pytest.mark.parametrize("num1, num2, expected", [
        (Decimal('5'), Decimal('3'), Decimal('2')),
        (Decimal('3'), Decimal('5'), Decimal('-2')),
        (Decimal('0'), Decimal('0'), Decimal('0')),
        (Decimal('0.3'), Decimal('0.1'), Decimal('0.2')),
    ])
    def test_subtract(self, num1, num2, expected):
        """Test subtraction operation with various inputs."""
        assert subtract(num1, num2) == expected

    @pytest.mark.parametrize("num1, num2, expected", [
        (Decimal('5'), Decimal('3'), Decimal('15')),
        (Decimal('-2'), Decimal('3'), Decimal('-6')),
        (Decimal('0'), Decimal('5'), Decimal('0')),
        (Decimal('0.1'), Decimal('0.2'), Decimal('0.02')),
    ])
    def test_multiply(self, num1, num2, expected):
        """Test multiplication operation with various inputs."""
        assert multiply(num1, num2) == expected

    @pytest.mark.parametrize("num1, num2, expected", [
        (Decimal('6'), Decimal('3'), Decimal('2')),
        (Decimal('5'), Decimal('2'), Decimal('2.5')),
        (Decimal('0'), Decimal('5'), Decimal('0')),
        (Decimal('1'), Decimal('3'), Decimal('0.3333333333333333333333333333')),
    ])
    def test_divide(self, num1, num2, expected):
        """Test division operation with various inputs."""
        assert divide(num1, num2) == expected

    def test_divide_by_zero(self):
        """Test division by zero raises appropriate exception."""
        with pytest.raises(ZeroDivisionError):
            divide(Decimal('5'), Decimal('0'))
