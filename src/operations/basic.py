from src.core.operation_registry import register_operation
from src.core.logging_decorator import log_method

@register_operation
@log_method
def add(a, b):
    return a + b

@register_operation
@log_method
def subtract(a, b):
    return a - b

@register_operation
@log_method
def multiply(a, b):
    return a * b

@register_operation
@log_method
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b