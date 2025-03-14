"""
Module for configuring application logging based on environment variables or a config file.
"""
import os
import sys
import logging
import logging.config
import logging.handlers


class LoggingConfigurator:
    """
    Handles the configuration of logging for the application.
    Supports configuration from either logging.conf or environment variables.
    
    Users only need to set:
    - LOG_LEVEL_CONSOLE: Level for console output (WARNING by default)
    - LOG_LEVEL_FILE: Level for file output (DEBUG by default)
    """

    @staticmethod
    def configure():
        """
        Configure logging for the application.
        
        This method sets up logging with:
        - Console output (WARNING level by default)
        - File output (DEBUG level by default)
        
        The log level can be configured through:
        1. A logging.conf file (if present)
        2. Environment variables LOG_LEVEL_CONSOLE and LOG_LEVEL_FILE
        """
        # Create logs directory if it doesn't exist
        log_dir = os.getenv("LOG_DIR", "logs")
        os.makedirs(log_dir, exist_ok=True)

        # Determine if we should use logging.conf or environment variables
        use_env_config = os.getenv("USE_ENV_LOGGING", "false").lower() == "true"

        if not use_env_config and os.path.exists("logging.conf"):
            # Use the logging.conf file
            logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
            logging_configuration = "configured from logging.conf"
        else:
            # Configure logging from environment variables
            LoggingConfigurator._configure_from_env(log_dir)
            logging_configuration = "configured from environment variables"

        logging.info(f"Logging {logging_configuration}")

    @staticmethod
    def _configure_from_env(log_dir):
        """
        Configure logging based on environment variables.
        
        Users only need to set:
        - LOG_LEVEL_CONSOLE: Level for console output
        - LOG_LEVEL_FILE: Level for file output
        
        Internal loggers are automatically configured appropriately.

        Args:
            log_dir: Directory where log files will be stored
        """
        # User-configurable settings
        console_level = os.getenv("LOG_LEVEL_CONSOLE", "WARNING")
        file_level = os.getenv("LOG_LEVEL_FILE", "DEBUG")
        log_filename = os.path.join(log_dir, os.getenv("LOG_FILENAME", "app.log"))
        
        # Clear all existing handlers from the root logger
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
            
        # Set root level to the lowest of console/file to allow all messages through
        lowest_level = min(
            getattr(logging, console_level), 
            getattr(logging, file_level)
        )
        root_logger.setLevel(lowest_level)
        
        # Configure internal loggers (hidden from user)
        # These settings ensure decorator logging works as intended
        _configure_internal_loggers()

        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            '%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            '%Y-%m-%d %H:%M:%S'
        )

        # File handler (detailed format with class names)
        file_handler = logging.handlers.RotatingFileHandler(
            log_filename, 'a', 1048576, 5
        )
        file_handler.setLevel(getattr(logging, file_level))
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)

        # Console handler (simple format without class names)
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(getattr(logging, console_level))
        console_handler.setFormatter(simple_formatter)
        root_logger.addHandler(console_handler)


def _configure_internal_loggers():
    """
    Configure internal loggers needed by the class decorator system.
    This is hidden implementation detail not exposed to users.
    """
    # Configure trace logger for function entry/exit
    trace_logger = logging.getLogger('trace')
    trace_logger.propagate = True
    
    # Configure src logger for application classes
    src_logger = logging.getLogger('src')
    src_logger.propagate = True