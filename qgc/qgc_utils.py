# qgc/qgc_utils.py

import logging
import json
import numpy as np
import yaml
import os

# Configure logging for utility functions
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_measurement(measurement, min_value, max_value):
    """
    Validate a gravitational measurement against specified limits.

    :param measurement: The gravitational measurement to validate.
    :param min_value: The minimum acceptable value.
    :param max_value: The maximum acceptable value.
    :return: True if valid, False otherwise.
    """
    if min_value <= measurement <= max_value:
        logger.info(f"Measurement {measurement:.4f} m/s^2 is valid.")
        return True
    else:
        logger.warning(f"Measurement {measurement:.4f} m/s^2 is out of range ({min_value:.4f}, {max_value:.4f}).")
        return False

def calculate_statistics(measurements):
    """
    Calculate mean and standard deviation of a list of measurements.

    :param measurements: List of gravitational measurements.
    :return: A dictionary containing mean and standard deviation.
    """
    if not measurements:
        logger.warning("No measurements provided for statistics calculation.")
        return {"mean": None, "std_dev": None}

    mean = np.mean(measurements)
    std_dev = np.std(measurements)
    logger.info(f"Calculated statistics: Mean = {mean:.4f}, Std Dev = {std_dev:.4f}")
    return {"mean": mean, "std_dev": std_dev}

def log_json(data, message="Data"):
    """
    Log a JSON-serializable object.

    :param data: The data to log.
    :param message: A message to accompany the log entry.
    """
    try:
        json_data = json.dumps(data, indent=4)
        logger.info(f"{message}: {json_data}")
    except (TypeError, ValueError) as e:
        logger.error(f"Failed to serialize data to JSON: {e}")

def load_config(config_file):
    """
    Load configuration from a YAML file.

    :param config_file: Path to the configuration file.
    :return: Parsed configuration data.
    """
    if not os.path.exists(config_file):
        logger.error(f"Configuration file {config_file} does not exist.")
        return None

    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"Configuration loaded from {config_file}.")
            return config
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration file {config_file}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading configuration file {config_file}: {e}")
        return None

def save_to_file(data, file_path):
    """
    Save data to a file in JSON format.

    :param data: The data to save.
    :param file_path: The path to the file where data will be saved.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            logger.info(f"Data saved to {file_path}.")
    except Exception as e:
        logger.error(f"Error saving data to file {file_path}: {e}")

def transform_measurements(measurements, transformation_func):
    """
    Apply a transformation function to a list of measurements.

    :param measurements: List of gravitational measurements.
    :param transformation_func: Function to apply to each measurement.
    :return: List of transformed measurements.
    """
    try:
        transformed = [transformation_func(m) for m in measurements]
        logger.info(f"Transformed measurements: {transformed}")
        return transformed
    except Exception as e:
        logger.error(f"Error transforming measurements: {e}")
        return []

def generate_report(statistics, file_path):
    """
    Generate a report of the statistics and save it to a file.

    :param statistics: Dictionary containing statistics to report.
    :param file_path: Path to the report file.
    """
    report = {
        "Statistics Report": {
            "Mean": statistics.get("mean"),
            "Standard Deviation": statistics.get("std_dev"),
            "Timestamp": logger.handlers[0].formatter._fmt
        }
    }
    save_to_file(report, file_path)

# Example utility function usage
if __name__ == "__main__":
    # Validate a measurement
    valid = validate_measurement(9.81, 9.70, 9.90)
    print(f"Measurement valid: {valid}")

    # Calculate statistics
    stats = calculate_statistics([9.78, 9.81, 9.79, 9.82, 9.75])
    print(f"Statistics: {stats}")

    # Log JSON data
    log_json({"key": "value", "another_key": 123}, "Sample JSON Data")

    # Load configuration
    config = load_config("qgc/qgc_config.yaml")
    print(f"Loaded Config: {config}")

    # Save data to file
    save_to_file({"example_key": "example_value"}, "example_output.json")

    # Transform measurements
    transformed_measurements = transform_measurements([9.78, 9.81, 9.79], lambda x: x * 1.01)
    print(f"Transformed Measurements: {transformed_measurements}")

    # Generate a report
    generate_report(stats, "statistics_report.json")
