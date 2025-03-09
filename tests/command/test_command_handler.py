"""
Test the CommandHandler class.
"""
# pylint: disable=protected-access
# Used for testing purposes only.
from calculator.command.command_handler import CommandHandler


def test_register_command(mock_command):
    """Test that a command is correctly registered."""
    handler = CommandHandler()
    handler._register("test", mock_command)

    assert "test" in handler._commands
    assert handler._commands["test"] is mock_command


def test_execute_registered_command(mock_command):
    """Test that a registered command executes properly."""
    handler = CommandHandler()
    handler._register("test", mock_command)

    handler.handle("test")
    assert mock_command.executed is True


def test_execute_unregistered_command(capfd):
    """Test that handling an unregistered command prints an error."""
    handler = CommandHandler()

    handler.handle("nonexistent")

    captured = capfd.readouterr()
    assert 'Command "nonexistent" not found' in captured.out


def test_dynamic_command_discovery(mock_command_package, mock_greet_class, mock_exit_class):
    """
    Test that the CommandHandler dynamically discovers and registers commands
    using the mocked package fixture.
    """
    handler = CommandHandler()
    handler.load_commands(mock_command_package)  # Load commands dynamically

    # Ensure the mocked commands were registered
    assert "greet" in handler._commands
    assert "exit" in handler._commands

    # Ensure they are instances of the mocked command classes
    assert isinstance(handler._commands["greet"], mock_greet_class)
    assert isinstance(handler._commands["exit"], mock_exit_class)


def test_help_command(capsys, mock_command):
    """
    Test that the help command prints all available commands.
    """
    handler = CommandHandler()
    # Register a dummy command for testing.
    handler._register("mock", mock_command)
    # Execute the help command.
    handler._commands["help"].execute()
    captured = capsys.readouterr().out
    # The output should list both "dummy" and "help"
    assert "mock" in captured
    assert "help" in captured

def test_suggest_command_found(capsys, mock_command):
    """
    Test that when an invalid command that is similar to an existing one is entered,
    the handler prints a suggestion and does not invoke the help command.
    """
    handler = CommandHandler()
    # Register a dummy command "add".
    handler._register("add", mock_command)
    # Available commands: "add" and "help"
    # When user types "ad", we expect a suggestion for "add"
    handler.handle("ad")
    captured = capsys.readouterr().out
    # The suggestion should be printed:
    assert 'Did you mean "add"?' in captured
    # Since a suggestion was found, help is not invoked (its output not present)
    assert "Available commands:" not in captured

def test_suggest_command_failed(capsys):
    """
    Test that when an invalid command with no close match is entered,
    the handler prints a default not found message and invokes the help command.
    """
    handler = CommandHandler()
    # Only "help" is registered by default.
    # When entering an unrelated command (e.g., "xyz"), no suggestion is found.
    handler.handle("xyz")
    captured = capsys.readouterr().out
    # The output should indicate the command was not found.
    assert 'Command "xyz" not found' in captured
    # And then the help command output should be printed.
    assert "Available commands:" in captured
