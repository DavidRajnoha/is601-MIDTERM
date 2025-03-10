"""
DivideCommand class module.
"""
from src.command.command import Command
from src.coordination.operation_executor import BinaryOperationExecutor
from src.core.logging import log_class
from src.operations.basic import divide

@log_class
class DivideCommand(Command):
    """
    A command that performs division.
    """
    def __init__(self, executor=None):
        """
        Initializes the DivideCommand with an optional OperationExecutor.
        """
        self.executor = executor or BinaryOperationExecutor(divide, "Division")

    def execute(self):
        """
        Executes the command.
        """
        self.executor.execute()