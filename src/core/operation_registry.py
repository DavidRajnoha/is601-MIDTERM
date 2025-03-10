operation_registry = {}

def register_operation(func):
    """Decorator to register an operation function using its name."""
    operation_registry[func.__name__] = func
    return func