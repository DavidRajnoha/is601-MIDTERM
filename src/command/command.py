from abc import ABC, abstractmethod


class Command(ABC):
    """
    Command interface declares a method for executing a command.
    """
    @abstractmethod
    def execute(self):
        pass


class ExitException(Exception):
    pass