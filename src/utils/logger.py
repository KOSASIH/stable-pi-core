import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file, level=logging.INFO, max_bytes=5*1024*1024, backup_count=5):
    """Function to set up a logger with file and console output."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a rotating file handler
    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    handler.setLevel(level)

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)
    logger.addHandler(console_handler)

    return logger

def log_exception(logger):
    """Log an exception with traceback."""
    import traceback
    logger.error("An exception occurred", exc_info=True)

# Example usage
if __name__ == "__main__":
    log_file = os.getenv('LOG_FILE', 'app.log')  # Use environment variable or default to 'app.log'
    log = setup_logger('api_logger', log_file)
    log.info('Logger is set up and ready to use.')

    # Example of logging an exception
    try:
        1 / 0  # This will raise a ZeroDivisionError
    except Exception as e:
        log_exception(log)
