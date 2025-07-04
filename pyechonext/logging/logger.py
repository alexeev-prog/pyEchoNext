import logging
import sys
from typing import Optional


class LoggerManager:
    """Manager for configuring and handling logging in the application.

    This class is responsible for creating and managing instances of loggers,
    allowing users to configure log levels, handlers, and formats easily. Each
    LoggerManager instance can set up a dedicated logger for a particular
    usage context.

    Attributes:
                    logger (logging.Logger): The logger instance configured for the library.
                    handlers_configured (bool): Flag indicating if the handlers have been set up.
    """

    def __init__(self):
        """Initializes the LoggerManager instance with a logger and default configuration.

        The constructor sets up a logger for the "pyechonext" namespace and applies
        the default logging configuration.
        """
        self.logger = logging.getLogger("pyechonext")
        self.handlers_configured = False
        self.configure_logging()  # Default configuration

    def configure_logging(
        self,
        level: int = logging.INFO,
        stream_handler: bool = True,
        file_handler: Optional[str] = None,
        formatter: Optional[logging.Formatter] = None,
    ):
        """Configures the logging settings for the logger.

        This method sets the log level, specifies if a stream handler should be
        added, and optionally allows for a file handler and a specific message
        format.

        Args:
            level (int): The logging level to set for the logger (default: logging.INFO).
            stream_handler (bool): Flag to indicate if output to stdout should occur (default: True).
            file_handler (Optional[str]): Path to a file where logs will be written (default: None).
            formatter (Optional[logging.Formatter]): A formatter instance for custom log message formatting (default: None).
        """
        self.logger.setLevel(level)
        self.clear_handlers()  # Clear existing handlers before adding new ones

        # Use the provided formatter or a default one
        formatter = formatter or self.default_formatter()

        # Add stream handler if specified
        if stream_handler:
            self.add_handler(logging.StreamHandler(sys.stdout), formatter)

        # Add file handler if a file path is provided
        if file_handler:
            self.add_handler(logging.FileHandler(file_handler), formatter)

    def default_formatter(self) -> logging.Formatter:
        """Returns the default log message formatter.

        The default formatter outputs the log messages with the format:
        'timestamp - logger name - log level - message'.

        Returns:
            logging.Formatter: The default formatter for log messages.
        """
        return logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def clear_handlers(self):
        """Removes all existing handlers from the logger.

        This method ensures that the logger starts with a clean slate before new
        handlers are added, preventing duplicate log messages and improving
        configuration consistency.
        """
        self.logger.handlers.clear()

    def add_handler(self, handler: logging.Handler, formatter: logging.Formatter):
        """Adds a new handler to the logger with a specified formatter.

        This method attaches a logging handler (either stream or file) to the
        logger and sets its message format.

        Args:
            handler (logging.Handler): The logging handler to add (e.g., StreamHandler).
            formatter (logging.Formatter): The formatter to set for the handler.
        """
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def set_log_level(self, level: int):
        """Sets the logging level for the logger.

        This method allows dynamic adjustments to the logging level at runtime.

        Args:
            level (int): The new logging level to set for the logger.
        """
        self.logger.setLevel(level)

    def get_logger(self) -> logging.Logger:
        """Retrieves the configured logger instance.

        Returns:
            logging.Logger: The logger instance configured for the library.
        """
        return self.logger


def create_logger(
    level: int = logging.INFO,
    stream_handler: bool = True,
    file_handler: Optional[str] = None,
    formatter: Optional[logging.Formatter] = None,
) -> logging.Logger:
    """Creates and configures a new logger instance.

    This function instantiates a LoggerManager, applies the specified logging
    configuration, and returns the logger for further use.

    Args:
        level (int): The logging level to set for the logger (default: logging.INFO).
        stream_handler (bool): Flag to indicate if output to stdout should occur (default: True).
        file_handler (Optional[str]): Path to a file where logs will be written (default: None).
        formatter (Optional[logging.Formatter]): A formatter instance for custom log message formatting (default: None).

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger_manager = LoggerManager()
    logger_manager.configure_logging(
        level, stream_handler, file_handler, formatter)
    return logger_manager.get_logger()
