"""
Defines a decorator to log function calls and exceptions.
https://ankitbko.github.io/blog/2021/04/logging-in-python/
"""
import functools
import inspect
import logging

trace_logger = logging.getLogger("trace")

def log_method(func):
    """
    Decorator that logs method entry/exit and exceptions at the trace level.
    This is for technical tracing of code execution flow, not business logic.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        trace_logger.debug(f"function {func.__name__} called with args {signature}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # Only log the exception at trace level since this is part of execution tracing
            trace_logger.debug(f"Exception raised in {func.__name__}. exception: {str(e)}")
            raise e
    return wrapper

def get_class_logger(cls):
    """
    Get or create a class-specific logger.
    This makes it easier to filter logs by component/class.
    """
    logger_name = f"{cls.__module__}.{cls.__name__}"
    return logging.getLogger(logger_name)

def log_class(cls):
    """
    Class decorator that applies the log decorator to all methods of a class.
    Also adds a logger property to the class for component-specific logging.
    """
    # Add class-specific logger that can be used for business logic logs
    cls.logger = get_class_logger(cls)
    
    for name, method in inspect.getmembers(cls, inspect.isfunction):
        # Skip special methods (like __init__, __str__, etc.)
        if not name.startswith('__') or name == '__init__':
            setattr(cls, name, log_method(method))
    return cls
