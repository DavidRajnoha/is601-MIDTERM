"""
This module contains tests for the command module.
"""

import pytest
from calculator.command.commands.exit import ExitCommand
from calculator.command.commands.greet import GreetCommand
from calculator.command.command import ExitException


def test_exit_command_raises_exception():
    """
    Test that the ExitCommand raises ExitException when executed.
    """
    exit_command = ExitCommand()

    with pytest.raises(ExitException) as excinfo:
        exit_command.execute()

    assert isinstance(excinfo.value, ExitException)


def test_greet_command_output(capfd):
    """
    Test that the GreetCommand prints the correct message.
    """
    greet_command = GreetCommand()
    greet_command.execute()

    captured = capfd.readouterr()
    assert "Hello, World!" in captured.out
