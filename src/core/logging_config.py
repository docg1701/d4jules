import logging
import sys

def setup_logging(level=logging.INFO):
    """
    Configures structured logging for the application.
    """
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Create a handler for stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Create a formatter and add it to the handler
    # Example format: 2023-10-27 14:35:07,123 - INFO - module_name - Log message
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    # Add the handler to the root logger
    # Avoid adding handler if already present (e.g., during reloads or multiple calls)
    if not any(isinstance(h, logging.StreamHandler) and h.stream == sys.stdout for h in root_logger.handlers):
        root_logger.addHandler(handler)

if __name__ == '__main__':
    # Example usage:
    setup_logging(logging.DEBUG)

    logger = logging.getLogger(__name__)
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("This is an exception message.")

    # Example of a logger from another module
    another_module_logger = logging.getLogger("another.module")
    another_module_logger.info("Info from another module.")
