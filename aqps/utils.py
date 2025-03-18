import logging
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_logging(log_level=None):
    """
    Set up logging configuration.

    :param log_level: Optional logging level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    """
    if log_level:
        logging.getLogger().setLevel(log_level)
        logging.info(f"Logging level set to {log_level}")

def log_error(message):
    """
    Log an error message.

    :param message: The error message to log
    """
    logging.error(message)

def log_info(message):
    """
    Log an informational message.

    :param message: The informational message to log
    """
    logging.info(message)

def handle_exception(e):
    """
    Handle exceptions by logging the error and exiting the program.

    :param e: The exception to handle
    """
    log_error(f"An error occurred: {str(e)}")
    sys.exit(1)

def validate_environment_variables(required_vars):
    """
    Validate that all required environment variables are set.

    :param required_vars: A list of required environment variable names
    :raises EnvironmentError: If any required variable is not set
    """
    missing_vars = [var for var in required_vars if var not in os.environ]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

def generate_unique_id():
    """
    Generate a unique identifier (UUID).

    :return: A unique identifier as a string
    """
    import uuid
    return str(uuid.uuid4())

if __name__ == "__main__":
    # Example usage
    try:
        setup_logging()
        validate_environment_variables(['SATELLITE_API_URL', 'BLOCKCHAIN_API_URL'])
        log_info("All required environment variables are set.")
        unique_id = generate_unique_id()
        log_info(f"Generated unique ID: {unique_id}")
    except Exception as e:
        handle_exception(e)
