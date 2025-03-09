"""
Fixtures for command tests.
"""
# pylint: disable=redefined-outer-name

import importlib
import inspect
from unittest import mock
import pytest

from src.command.command import Command

class MockCommand(Command):
    """A mock command for testing purposes."""
    def __init__(self):
        self.executed = False

    def execute(self):
        self.executed = True

@pytest.fixture
def mock_command():
    """
    Fixture that sets up a mocked command for testing purposes.
    """
    return MockCommand()

@pytest.fixture
def mock_command_package(mock_command_discovery):
    """
    Fixture that sets up a mocked command package with dynamically discovered commands.
    """
    return mock_command_discovery["package"]

@pytest.fixture
def mock_exit_class(mock_command_discovery):
    """
    Fixture that sets up a mocked exit command class.
    """
    return mock_command_discovery["exit_class"]

@pytest.fixture
def mock_greet_class(mock_command_discovery):
    """
    Fixture that sets up a mocked greet command class.
    """
    return mock_command_discovery["greet_class"]

@pytest.fixture
def mock_command_discovery():
    """
    Fixture that sets up a mocked command package with dynamically discovered commands.
    Yields a dictionary containing:
      - "package": the mocked package,
      - "greet_class": the mock greet command class,
      - "exit_class": the mock exit command class.
    """
    # Save the real import_module so we can fall back for non-mocked modules.
    real_import_module = importlib.import_module

    mock_package = mock.Mock()
    mock_package.__name__ = "mocked_commands"
    mock_package.__path__ = ["mocked_commands"]

    class MockGreetCommand(Command):
        """A mock greet command for testing purposes."""
        def execute(self):
            print("Mock Greet")

    class MockExitCommand(Command):
        """A mock exit command for testing purposes."""
        def execute(self):
            pass

    # Create fake modules mimicking real command modules.
    mock_greet_module = mock.Mock()
    mock_greet_module.MockGreetCommand = MockGreetCommand

    mock_exit_module = mock.Mock()
    mock_exit_module.MockExitCommand = MockExitCommand

    # Simulate pkgutil.iter_modules() returning fake modules.
    fake_modules = [
        (None, "mocked_commands.greet", None),
        (None, "mocked_commands.exit", None),
    ]

    def mock_import_module(name):
        """Return a mocked module if available, else fall back to the real function."""
        mock_modules_dict = {
            "mocked_commands.greet": mock_greet_module,
            "mocked_commands.exit": mock_exit_module,
        }
        return mock_modules_dict[name] if name in mock_modules_dict else real_import_module(name)

    def mock_getmembers(mod, predicate):
        """Return members for our fake modules."""
        if mod is mock_greet_module:
            return [("MockGreetCommand", MockGreetCommand)]
        if mod is mock_exit_module:
            return [("MockExitCommand", MockExitCommand)]
        return inspect.getmembers(mod, predicate)

    with mock.patch("pkgutil.iter_modules", return_value=fake_modules), \
         mock.patch("importlib.import_module", side_effect=mock_import_module), \
         mock.patch("inspect.getmembers", side_effect=mock_getmembers):
        yield {
            "package": mock_package,
            "greet_class": MockGreetCommand,
            "exit_class": MockExitCommand,
        }
