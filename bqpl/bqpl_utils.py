# bqpl/bqpl_utils.py

import logging
import yaml

def load_config(config_file):
    """
    Load the configuration from a YAML file.

    :param config_file: Path to the configuration file.
    :return: Configuration dictionary.
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    logging.info(f"Loaded configuration from {config_file}")
    return config

def validate_biosensor_data(data):
    """
    Validate the data collected from the biosensor.

    :param data: The data to validate (dictionary).
    :return: Boolean indicating whether the data is valid.
    """
    if not isinstance(data, dict):
        logging.error("Biosensor data is not a dictionary.")
        return False

    required_keys = ['heart_rate', 'temperature']
    for key in required_keys:
        if key not in data:
            logging.error(f"Missing required key: {key}")
            return False

    if not (60 <= data['heart_rate'] <= 100):
        logging.error("Heart rate is out of valid range (60-100).")
        return False

    if not (36.0 <= data['temperature'] <= 38.5):
        logging.error("Temperature is out of valid range (36.0-38.5).")
        return False

    logging.info("Biosensor data is valid.")
    return True

def log_event(message, level="INFO"):
    """
    Log an event with the specified message and level.

    :param message: The message to log.
    :param level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    if level == "DEBUG":
        logging.debug(message)
    elif level == "WARNING":
        logging.warning(message)
    elif level == "ERROR":
        logging.error(message)
    elif level == "CRITICAL":
        logging.critical(message)
    else:
        logging.info(message)

def convert_to_binary(data):
    """
    Convert biological data to a binary string.

    :param data: The biological data (dictionary).
    :return: A binary string representation of the data.
    """
    heart_rate_binary = format(data['heart_rate'], '08b')  # 8 bits for heart rate
    temperature_binary = format(int((data['temperature'] - 36) * 100), '08b')  # Scale temperature

    # Combine the binary representations
    binary_string = heart_rate_binary + temperature_binary
    logging.info(f"Converted data to binary: {binary_string}")
    return binary_string

# Example usage
if __name__ == "__main__":
    # Load configuration
    config = load_config("bqpl/bqpl_config.yaml")

    # Example biosensor data
    biosensor_data = {
        "heart_rate": 75,
        "temperature": 37.5
    }

    # Validate biosensor data
    if validate_biosensor_data(biosensor_data):
        # Convert to binary if valid
        binary_data = convert_to_binary(biosensor_data)
        print(f"Binary Representation: {binary_data}")
