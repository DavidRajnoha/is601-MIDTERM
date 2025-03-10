import logging
from typing import Callable, List, Union, Optional
from decimal import Decimal, InvalidOperation
import uuid
from datetime import datetime

from src.core.operation_registry import operation_registry

class Calculation:
    """
    Represents a calculation that uses an operation on multiple numbers.

    Attributes:
        id (str): Unique identifier for the calculation.
        operation (Callable[..., Decimal]): The operation to perform on operands.
        operands (List[Decimal]): The list of operands.
        result (Optional[Decimal]): The result of the calculation (None until perform_operation is called).
        timestamp (datetime): When the calculation was created.
    """
    def __init__(self, operation: Callable[..., Decimal], *args: Union[Decimal, int, float, str]):
        """
        Initializes the Calculation with a specific operation and variable number of operands.

        Args:
            operation (Callable[..., Decimal]): The operation to perform.
            *args: Variable length list of operands that will be converted to Decimal.
        
        Raises:
            ValueError: If no operands are provided.
        """
        if len(args) == 0:
            raise ValueError("At least one operand must be provided")
            
        self.id = str(uuid.uuid4())
        self.operation = operation
        self.operands = [Decimal(str(arg)) for arg in args]
        self.result: Optional[Decimal] = None
        self.timestamp = datetime.now()
        self.operation_name = operation.__name__ if hasattr(operation, "__name__") else "unknown_operation"

    def perform_operation(self) -> Decimal:
        """
        Performs the calculation using the provided operation on the operands.
        Stores the result in the calculation object.

        Returns:
            Decimal: The result of applying the operation to all operands.

        Raises:
            Exception: Propagates any exception raised by the operation.
        """
        try:
            self.result = self.operation(*self.operands)
        except TypeError as e:
            raise e

        return self.result
        
    def __str__(self) -> str:
        """Return a string representation of the calculation."""
        operands_str = ', '.join(str(op) for op in self.operands)
        result_str = f" = {self.result}" if self.result is not None else ""
        return f"{self.operation_name}({operands_str}){result_str}"

    def to_dict(self) -> dict:
        """Convert the Calculation object to a dictionary."""
        return {
            'id': self.id,
            'operation_name': self.operation_name,
            'operands': ','.join(str(op) for op in self.operands),
            'result': str(self.result) if self.result is not None else "",
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Calculation':
        """Create calculation from dictionary representation."""
        try:
            operands = [Decimal(op) for op in data['operands'].split(',')]
        except InvalidOperation:
            logging.debug(f"Invalid operand value: {data['operands']}")
            raise ValueError("Invalid operand value")

        operation_name = data['operation_name']

        if operation_name not in operation_registry:
            raise ValueError(f"Unknown operation: {operation_name}")

        operation = operation_registry[operation_name]

        calc = cls(operation, *operands)
        calc.id = data['id']
        calc.result = Decimal(data['result']) if data['result'] else None
        calc.timestamp = datetime.fromisoformat(data['timestamp'])

        return calc
