"""
MultiplyCommand class module.
"""
from src.command.command import Command
from src.coordination.operation_executor import BinaryOperationExecutor
from src.operations.basic import multiply


class MultiplyCommand(Command):
    """
    A command that performs multiplication.
    """
    def __init__(self, executor=None):
        """
        Initializes the MultiplyCommand with an optional OperationExecutor.
        """
        self.executor = executor or BinaryOperationExecutor(multiply, "Multiplication")

    def execute(self):
        """
        Executes the command.
        """
        self.executor.execute()