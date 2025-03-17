import logging
import os
import json

def setup_logging(log_file='emotion_responsive_ai.log'):
    """
    Sets up logging for the emotion-responsive AI module.

    Args:
        log_file (str): The name of the log file to write logs to.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Logging is set up for Emotion-Responsive AI Module.")

def log_event(event_message):
    """
    Logs an event message.

    Args:
        event_message (str): The message to log.
    """
    logging.info(event_message)

def handle_error(error_message):
    """
    Logs an error message and raises an exception.

    Args:
        error_message (str): The error message to log.
    
    Raises:
        Exception: Raises an exception with the provided error message.
    """
    logging.error(error_message)
    raise Exception(error_message)

def check_storage_capacity(current_usage, storage_capacity):
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

def create_directory(directory):
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

def save_json(data, file_path):
    """
    Saves data to a JSON file.

    Args:
        data (dict): The data to save.
        file_path (str): The path of the file to save the data to.
    """
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    logging.info(f"Data saved to JSON file: {file_path}")

def load_json(file_path):
    """
    Loads data from a JSON file.

    Args:
        file_path (str): The path of the file to load the data from.

    Returns:
        dict: The loaded data.
    """
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    logging.info(f"Data loaded from JSON file: {file_path}")
    return data
