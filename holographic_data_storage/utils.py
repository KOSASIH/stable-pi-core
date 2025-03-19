import logging
import os

def setup_logging(log_file: str = 'holographic_storage.log'):
    """
    Sets up logging for the holographic data storage module.

    Args:
        log_file (str): The name of the log file to write logs to.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Logging is set up.")

def log_event(event_message: str):
    """
    Logs an event message.

    Args:
        event_message (str): The message to log.
    """
    logging.info(event_message)

def handle_error(error_message: str):
    """
    Logs an error message and raises an exception.

    Args:
        error_message (str): The error message to log.
    
    Raises:
        Exception: Raises an exception with the provided error message.
    """
    logging.error(error_message)
    raise Exception(error_message)

def check_storage_capacity(current_usage: int, storage_capacity: int) -> bool:
    """
    Checks if there is enough storage capacity available.

    Args:
        current_usage (int): The current usage of the storage in bytes.
        storage_capacity (int): The maximum capacity of the storage in bytes.

    Returns:
        bool: True if there is enough capacity, False otherwise.
    """
    if current_usage >= storage_capacity:
        logging.warning("Not enough storage capacity available.")
        return False
    return True

def create_directory(directory: str):
    """
    Creates a directory if it does not exist.

    Args:
        directory (str): The path of the directory to create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Directory created: {directory}")
    else:
        logging.info(f"Directory already exists: {directory}")
