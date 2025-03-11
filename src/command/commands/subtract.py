"""
SubtractCommand class module.
"""
from src.command.command import Command
from src.coordination.operation_executor import BinaryOperationExecutor
from src.core.logging_decorator import log_class
from src.operations.basic import subtract

@log_class
class SubtractCommand(Command):
    """
    A command that performs subtraction.
    """
    def __init__(self, executor=None):
        """
        Initializes the SubtractCommand with an optional OperationExecutor.
        """
        self.executor = executor or BinaryOperationExecutor(subtract, "Subtraction")

    def execute(self):
        """
        Executes the command.
        """
        self.executor.execute()