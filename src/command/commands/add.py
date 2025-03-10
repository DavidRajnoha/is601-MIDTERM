"""
AddCommand class module.
"""
from src.command.command import Command
from src.coordination.operation_executor import BinaryOperationExecutor
from src.core.logging import log_class
from src.operations.basic import add


@log_class
class AddCommand(Command):
    """
    A command that performs addition.
    """
    def __init__(self, executor=None):
        """
        Initializes the AddCommand with an optional OperationExecutor.
        """
        self.executor = executor or BinaryOperationExecutor(add, "Addition")

    def execute(self):
        """
        Executes the command.
        """
        self.executor.execute()