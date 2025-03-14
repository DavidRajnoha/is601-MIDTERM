"""Tests for history-related commands."""
# pylint: disable=redefined-outer-name

from src.command.commands.clear_history import ClearHistoryCommand


def test_clear_history_command(mock_history):
    """Test clear history command."""
    command = ClearHistoryCommand(mock_history)
    result = command.execute()

    mock_history.clear_history.assert_called_once()
    assert "cleared" in result.lower()
