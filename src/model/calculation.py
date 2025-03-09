from typing import Callable, List, Union
from decimal import Decimal

class Calculation:
    """
    Represents a calculation that uses an operation on multiple numbers.

    Attributes:
        operation (Callable[[Decimal, Decimal], Decimal]): A function that takes two Decimals and returns a Decimal.
        operands (List[Decimal]): The list of operands.
    """
    def __init__(self, operation: Callable[..., Decimal], *args: Union[Decimal, int, float, str]):
        """
        Initializes the Calculation with a specific operation and variable number of operands.

        Args:
            operation (Callable[[Decimal, Decimal], Decimal]): The operation to perform.
            *args: Variable length list of operands that will be converted to Decimal.
        
        Raises:
            ValueError: If no operands are provided.
        """
        if len(args) == 0:
            raise ValueError("At least one operand must be provided")
            
        self.operation = operation
        self.operands = [Decimal(str(arg)) for arg in args]

    def perform_operation(self) -> Decimal:
        """
        Performs the calculation using the provided operation on the operands.
        For binary operations, applies the operation cumulatively from left to right.

        Returns:
            Decimal: The result of applying the operation to all operands.

        Raises:
            Exception: Propagates any exception raised by the operation.
        """
        try:
            result = self.operation(*self.operands)
        except TypeError as e:
            raise e

        return result
