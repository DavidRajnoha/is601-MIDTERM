from decimal import Decimal

from src.core.logging import log_method


@log_method
def add(a: Decimal, b: Decimal) -> Decimal:
    return a + b

@log_method
def subtract(a: Decimal, b: Decimal) -> Decimal:
    return a - b

@log_method
def multiply(a: Decimal, b: Decimal) -> Decimal:
    return a * b

@log_method
def divide(a: Decimal, b: Decimal) -> Decimal:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")

    return a / b