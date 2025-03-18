# dmec/utils.py

import logging
import os

def setup_logging(log_level=logging.INFO):
    """
    Set up the logging configuration for the application.
    :param log_level: The logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Logging is set up.")

def validate_positive(value, name):
    """
    Validate that a given value is positive.
    :param value: The value to validate.
    :param name: The name of the value (for logging purposes).
    :raises ValueError: If the value is not positive.
    """
    if value <= 0:
        logging.error(f"{name} must be positive. Provided value: {value}")
        raise ValueError(f"{name} must be positive. Provided value: {value}")

def ensure_directory_exists(directory):
    """
    Ensure that a directory exists; if not, create it.
    :param directory: The directory path to check.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")
    else:
        logging.info(f"Directory already exists: {directory}")

def format_timestamp(timestamp):
    """
    Format a timestamp into a human-readable string.
    :param timestamp: The timestamp to format.
    :return: A formatted string representation of the timestamp.
    """
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def load_json_file(filepath):
    """
    Load data from a JSON file.
    :param filepath: The path to the JSON file.
    :return: The data loaded from the JSON file.
    :raises FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, 'r') as f:
        data = json.load(f)
    logging.info(f"Loaded data from {filepath}")
    return data

def save_json_file(filepath, data):
    """
    Save data to a JSON file.
    :param filepath: The path to the JSON file.
    :param data: The data to save.
    """
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    logging.info(f"Saved data to {filepath}")
