"""
Tests for Calculator Command classes using OperationExecutor.

These tests cover:
  - Valid numeric input processing.
  - Handling of invalid input.
  - Handling division by zero.
  - Verification that each operation command (Add, Subtract, Multiply, Divide)
    correctly delegates to the OperationExecutor.
"""

# pylint: disable=invalid-name

from decimal import Decimal
from src.coordination.operation_executor import BinaryOperationExecutor as OperationExecutor
from src.command.commands.add import AddCommand
from src.command.commands.subtract import SubtractCommand
from src.command.commands.multiply import MultiplyCommand
from src.command.commands.divide import DivideCommand


def dummy_add(a: Decimal, b: Decimal) -> Decimal:
    """Return the sum of two Decimal numbers."""
    return a + b


def dummy_subtract(a: Decimal, b: Decimal) -> Decimal:
    """Return the difference of two Decimal numbers."""
    return a - b


def dummy_multiply(a: Decimal, b: Decimal) -> Decimal:
    """Return the product of two Decimal numbers."""
    return a * b


def dummy_divide(a: Decimal, b: Decimal) -> Decimal:
    """
    Return the quotient of two Decimal numbers.

    May raise ZeroDivisionError if b is zero.
    """
    return a / b


def test_operation_executor_valid(monkeypatch, capsys):
    """Test that OperationExecutor correctly processes valid input and prints the correct result."""
    executor = OperationExecutor(dummy_add, "Dummy Addition")
    inputs = iter(["3", "4"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    executor.execute()
    captured = capsys.readouterr().out
    # 3 + 4 = 7
    assert "Result of Dummy Addition: 7" in captured


def test_operation_executor_invalid(monkeypatch, capsys):
    """Test that OperationExecutor gracefully handles invalid input."""
    executor = OperationExecutor(dummy_add, "Dummy Addition")
    inputs = iter(["abc", "4"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    executor.execute()
    captured = capsys.readouterr().out
    assert "Invalid input" in captured


def test_operation_executor_zero_division(monkeypatch, capsys):
    """Test that OperationExecutor catches and reports a division by zero error."""
    executor = OperationExecutor(dummy_divide, "Dummy Division")
    inputs = iter(["10", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    executor.execute()
    captured = capsys.readouterr().out
    assert "Division by zero" in captured


def test_add_command(monkeypatch, capsys):
    """Test that the AddCommand correctly performs addition using its executor."""
    inputs = iter(["2", "3"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    command = AddCommand(OperationExecutor(dummy_add, "Addition"))
    command.execute()
    captured = capsys.readouterr().out
    # 2 + 3 = 5
    assert "Result of Addition: 5" in captured


def test_subtract_command(monkeypatch, capsys):
    """Test that the SubtractCommand correctly performs subtraction using its executor."""
    inputs = iter(["5", "3"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    command = SubtractCommand(OperationExecutor(dummy_subtract, "Subtraction"))
    command.execute()
    captured = capsys.readouterr().out
    # 5 - 3 = 2
    assert "Result of Subtraction: 2" in captured


def test_multiply_command(monkeypatch, capsys):
    """Test that the MultiplyCommand correctly performs multiplication using its executor."""
    inputs = iter(["4", "5"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    command = MultiplyCommand(OperationExecutor(dummy_multiply, "Multiplication"))
    command.execute()
    captured = capsys.readouterr().out
    # 4 * 5 = 20
    assert "Result of Multiplication: 20" in captured


def test_divide_command(monkeypatch, capsys):
    """Test that the DivideCommand correctly performs division using its executor."""
    inputs = iter(["20", "4"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    command = DivideCommand(OperationExecutor(dummy_divide, "Division"))
    command.execute()
    captured = capsys.readouterr().out
    # 20 / 4 = 5
    assert "Result of Division: 5" in captured


def test_divide_command_zero_division(monkeypatch, capsys):
    """Test that the DivideCommand correctly handles division by zero."""
    inputs = iter(["10", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    command = DivideCommand(OperationExecutor(dummy_divide, "Division"))
    command.execute()
    captured = capsys.readouterr().out
    assert "Division by zero" in captured
