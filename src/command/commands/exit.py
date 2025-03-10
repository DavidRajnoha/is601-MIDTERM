"""This module contains the ExitCommand class."""
import logging
from src.command.command import Command, ExitException
from src.core.logging import log_class


@log_class
class ExitCommand(Command):
    """A command that exits the application."""
    def execute(self):
        logging.debug("Executing ExitCommand.")
        raise ExitException()