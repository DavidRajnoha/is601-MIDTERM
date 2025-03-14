"""Tests for history-related commands."""
# pylint: disable=redefined-outer-name
from unittest.mock import patch

from src.command.commands.deletehistory import DeleteHistoryCommand
from src.exceptions.calculation_exceptions import  CalculationNotFoundError


def test_delete_history_command_with_input(mock_history):
    """Test delete history command with ID provided via user input."""
    # Set up the mocks
    mock_history.delete_calculation.return_value = None  # No return needed with EAFP

    with patch('builtins.input', return_value="calc1"):
        command = DeleteHistoryCommand(mock_history)
        result = command.execute()

    mock_history.delete_calculation.assert_called_once_with("calc1")
    assert "has been deleted" in result


def test_delete_history_command_empty_input(mock_history):
    """Test delete history command with empty input."""
    with patch('builtins.input', return_value=""):
        command = DeleteHistoryCommand(mock_history)
        result = command.execute()

    assert "Error" in result
    assert "provide" in result.lower()
    mock_history.delete_calculation.assert_not_called()


def test_delete_history_command_not_found(mock_history):
    """Test delete history command with ID that doesn't exist."""
    mock_history.delete_calculation.side_effect = CalculationNotFoundError("nonexistent_id")

    with patch('builtins.input', return_value="nonexistent_id"):
        command = DeleteHistoryCommand(mock_history)
        result = command.execute()

    assert "Error" in result
    assert "No calculation" in result
    mock_history.delete_calculation.assert_called_once_with("nonexistent_id")
