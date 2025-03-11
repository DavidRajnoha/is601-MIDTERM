"""Tests for history-related commands."""
# pylint: disable=redefined-outer-name

from src.command.commands.history import HistoryCommand



def test_history_command_empty(mock_history):
    """Test history command when there are no calculations."""

    command = HistoryCommand(mock_history)
    result = command.execute()

    assert "empty" in result.lower()
    mock_history.get_all_calculations.assert_called_once()


def test_history_command_with_data(mock_history, mock_calculations):
    """Test history command when there are calculations in history."""
    mock_history.get_all_calculations.return_value = mock_calculations

    command = HistoryCommand(mock_history)
    result = command.execute()

    mock_history.get_all_calculations.assert_called_once()
    assert "Calculation History" in result
    assert "calc1" in result
    assert "calc2" in result
