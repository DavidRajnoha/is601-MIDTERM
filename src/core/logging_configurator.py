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
    """

    @staticmethod
    def configure():
        """
        Configure logging based on either logging.conf file or environment variables.
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

        Args:
            log_dir: Directory where log files will be stored
        """
        root_level = os.getenv("LOG_LEVEL_ROOT", "DEBUG")
        trace_level = os.getenv("LOG_LEVEL_TRACE", "DEBUG")
        console_level = os.getenv("LOG_LEVEL_CONSOLE", "WARNING")
        file_level = os.getenv("LOG_LEVEL_FILE", "DEBUG")
        log_filename = os.path.join(log_dir, os.getenv("LOG_FILENAME", "app.log"))

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, root_level))

        # Configure trace logger
        trace_logger = logging.getLogger('trace')
        trace_logger.setLevel(getattr(logging, trace_level))
        trace_logger.propagate = False

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            '%Y-%m-%d %H:%M:%S'
        )

        # Remove any existing handlers
        for logger in [root_logger, trace_logger]:
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

        # File handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_filename, 'a', 1048576, 5
        )
        file_handler.setLevel(getattr(logging, file_level))
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(getattr(logging, console_level))
        console_handler.setFormatter(formatter)

        # Add handlers to loggers
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        trace_logger.addHandler(file_handler)
        trace_logger.addHandler(console_handler)