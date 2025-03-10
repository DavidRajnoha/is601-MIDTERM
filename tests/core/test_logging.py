import pytest
import logging
import io

from src.core.logging import log_method, log_class


@pytest.fixture
def logger_setup():
    """Fixture to set up and capture logs for testing."""
    # Create a StringIO object to capture log output
    log_capture = io.StringIO()

    # Create a handler that writes to the StringIO object
    handler = logging.StreamHandler(log_capture)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)

    # Get the logger used by the decorators and configure it
    logger = logging.getLogger('function.logger')
    logger.setLevel(logging.DEBUG)

    # Remove any existing handlers to avoid duplicate logs
    for hdlr in logger.handlers:
        logger.removeHandler(hdlr)

    logger.addHandler(handler)
    logger.propagate = False  # Prevent propagation to root logger

    yield logger, log_capture

    log_capture.close()
    logger.handlers.clear()


def test_log_method(logger_setup):
    """Test that a decorated function logs its call properly."""
    _, log_capture = logger_setup

    @log_method
    def test_function(a, b, c=None):
        return a + b

    result = test_function(1, 2, c="test")

    assert result == 3

    log_output = log_capture.getvalue()
    assert "function test_function called with args" in log_output
    assert "1, 2, c='test'" in log_output


def test_log_method_with_exception(logger_setup):
    """Test that a decorated function logs exceptions properly."""
    _, log_capture = logger_setup

    @log_method
    def failing_function():
        raise ValueError("Test error")

    with pytest.raises(ValueError, match="Test error"):
        failing_function()

    log_output = log_capture.getvalue()
    assert "Exception raised in failing_function" in log_output
    assert "Test error" in log_output


def test_log_class_initialization(logger_setup):
    """Test that a decorated class logs initialization properly."""
    _, log_capture = logger_setup

    @log_class
    class TestClass:
        def __init__(self, name):
            self.name = name

    TestClass("test_name")

    log_output = log_capture.getvalue()
    assert "function __init__ called with args" in log_output
    assert "test_name" in log_output


def test_log_class_methods(logger_setup):
    """Test that a decorated class logs all method calls."""
    _, log_capture = logger_setup

    @log_class
    class Calculator:
        def add(self, x, y):
            return x + y

        def multiply(self, x, y):
            return x * y

    calc = Calculator()
    assert calc.add(3, 4) == 7
    assert calc.multiply(5, 6) == 30

    log_output = log_capture.getvalue()

    assert "function add called with args" in log_output
    assert "function multiply called with args" in log_output


def test_log_class_with_exception(logger_setup):
    """Test that a decorated class logs method exceptions properly."""
    _, log_capture = logger_setup

    @log_class
    class BrokenCalculator:
        def divide(self, x, y):
            return x / y

    calc = BrokenCalculator()

    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)

    log_output = log_capture.getvalue()
    assert "Exception raised in divide" in log_output
