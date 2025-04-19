import logging

from pyechonext.logging.logger import create_logger

logger = create_logger(
    level=logging.DEBUG,
    file_handler="pyechonext.log",
    formatter=logging.Formatter("[%(asctime)s - %(levelname)s] - %(message)s"),
)

__all__ = [create_logger, logger]
