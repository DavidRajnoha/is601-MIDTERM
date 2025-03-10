"""
Defines a decorator to log function calls and exceptions.
https://ankitbko.github.io/blog/2021/04/logging-in-python/
"""
import functools
import inspect
import logging

logger = logging.getLogger("trace")

def log_method(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"function {func.__name__} called with args {signature}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # Not logging at error level as the exception is part of the normal flow.
            logger.debug(f"Exception raised in {func.__name__}. exception: {str(e)}")
            raise e
    return wrapper

def log_class(cls):
    """Class decorator that applies the log decorator to all methods of a class."""
    for name, method in inspect.getmembers(cls, inspect.isfunction):
        # Skip special methods (like __init__, __str__, etc.)
        if not name.startswith('__') or name == '__init__':
            setattr(cls, name, log_method(method))
    return cls
