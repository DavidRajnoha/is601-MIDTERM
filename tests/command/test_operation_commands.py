"""
Tests for Calculator Command classes using OperationExecutor.

These tests cover:
  - Valid numeric input processing.
  - Handling of invalid input.
  - Handling division by zero.
  - Verification that each operation command (Add, Subtract, Multiply, Divide)
    correctly delegates to the OperationExecutor.
"""
import pytest

from src.coordination.calculator import Calculator
# pylint: disable=invalid-name
# pylint: disable=redefined-outer-name


from src.coordination.operation_executor import BinaryOperationExecutor as OperationExecutor
from src.command.commands.add import AddCommand
from src.persistance.calculation_history import CalculationHistory


@pytest.fixture
def mock_history(mock_repository):
    """Return a CalculationHistory instance."""
    return CalculationHistory(mock_repository)


@pytest.fixture
def calculator(mock_history):
    """Return a Calculator instance."""
    return Calculator(mock_history)

def test_operation_executor_valid(monkeypatch, capsys, add_operation):
    """Test that OperationExecutor correctly processes valid input and prints the correct result."""
    executor = OperationExecutor(add_operation, "Dummy Addition")
    inputs = iter(["3", "4"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    executor.execute()
    captured = capsys.readouterr().out
    # 3 + 4 = 7
    assert "Result of Dummy Addition: 7" in captured


def test_operation_executor_invalid(monkeypatch, capsys, add_operation):
    """Test that OperationExecutor gracefully handles invalid input."""
    executor = OperationExecutor(add_operation, "Dummy Addition")
    inputs = iter(["abc", "4"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    executor.execute()
    captured = capsys.readouterr().out
    assert "Invalid input" in captured


def test_operation_executor_zero_division(monkeypatch, capsys, divide_operation):
    """Test that OperationExecutor catches and reports a division by zero error."""
    executor = OperationExecutor(divide_operation, "Dummy Division")
    inputs = iter(["10", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    executor.execute()
    captured = capsys.readouterr().out
    assert "The result of division by zero is not defined." in captured


def test_add_command(monkeypatch, capsys, add_operation):
    """Test that the AddCommand correctly performs addition using its executor."""
    inputs = iter(["2", "3"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    command = AddCommand(OperationExecutor(add_operation, "Addition"))
    command.execute()
    captured = capsys.readouterr().out
    # 2 + 3 = 5
    assert "Result of Addition: 5" in captured
