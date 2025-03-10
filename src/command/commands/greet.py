"""
A command that prints a greeting message.
"""
from src.command.command import Command
from src.core.logging import log_class


@log_class
class GreetCommand(Command):
    """A command that prints a greeting message."""
    def execute(self):
        print("Hello, World!")
