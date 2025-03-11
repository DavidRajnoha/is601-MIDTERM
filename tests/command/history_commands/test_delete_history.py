"""Tests for history-related commands."""
# pylint: disable=redefined-outer-name

from src.command.commands.deletehistory import DeleteHistoryCommand


def test_delete_history_command_with_input(mock_history, mock_calculations, monkeypatch):
    """Test delete history command with ID provided via user input."""
    mock_history.get_calculation_by_id.return_value = mock_calculations[0]
    mock_history.delete_calculation.return_value = True

    # Mock the input function to return "calc1"
    monkeypatch.setattr('builtins.input', lambda _: "calc1")

    command = DeleteHistoryCommand(mock_history)
    result = command.execute()

    mock_history.get_calculation_by_id.assert_called_once_with("calc1")
    mock_history.delete_calculation.assert_called_once_with("calc1")
    assert "has been deleted" in result


def test_delete_history_command_empty_input(mock_history, monkeypatch):
    """Test delete history command with empty input."""
    # Mock the input function to return an empty string
    monkeypatch.setattr('builtins.input', lambda _: "")

    command = DeleteHistoryCommand(mock_history)
    result = command.execute()

    assert "error" in result.lower()
    assert "provide" in result.lower()
    mock_history.delete_calculation.assert_not_called()


def test_delete_history_command_not_found(mock_history, monkeypatch):
    """Test delete history command with ID that doesn't exist."""
    mock_history.get_calculation_by_id.return_value = None

    command = DeleteHistoryCommand(mock_history)

    monkeypatch.setattr('builtins.input', lambda _: "nonexistent_id")
    result = command.execute()

    assert "error" in result.lower()
    assert "no calculation" in result.lower()
    mock_history.get_calculation_by_id.assert_called_once_with("nonexistent_id")
    mock_history.delete_calculation.assert_not_called()
