"""
A command that prints a greeting message.
"""
from src.command.command import Command


class GreetCommand(Command):
    """A command that prints a greeting message."""
    def execute(self):
        print("Hello, World!")
