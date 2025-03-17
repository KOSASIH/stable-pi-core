import json
import re
from typing import Any, Dict

def validate_sensor_data(data: Dict[str, Any]) -> bool:
    """
    Validates the sensor data to ensure it meets the required format.

    Args:
        data (Dict[str, Any]): The sensor data to validate.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    required_keys = ['sensor_id', 'timestamp', 'value', 'unit']
    for key in required_keys:
        if key not in data:
            print(f"Missing required key: {key}")
            return False

    if not isinstance(data['value'], (int, float)):
        print("Value must be a number.")
        return False

    if not isinstance(data['timestamp'], str) or not validate_timestamp(data['timestamp']):
        print("Invalid timestamp format.")
        return False

    return True

def validate_timestamp(timestamp: str) -> bool:
    """
    Validates the timestamp format.

    Args:
        timestamp (str): The timestamp to validate.

    Returns:
        bool: True if the timestamp is valid, False otherwise.
    """
    timestamp_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$'
    return re.match(timestamp_regex, timestamp) is not None

def format_sensor_data(sensor_id: str, value: float, unit: str) -> Dict[str, Any]:
    """
    Formats the sensor data into a standardized dictionary.

    Args:
        sensor_id (str): The ID of the sensor.
        value (float): The value collected from the sensor.
        unit (str): The unit of measurement.

    Returns:
        Dict[str, Any]: A dictionary containing the formatted sensor data.
    """
    from datetime import datetime

    return {
        "sensor_id": sensor_id,
        "timestamp": datetime.utcnow().isoformat() + 'Z',  # ISO 8601 format
        "value": value,
        "unit": unit
    }

def log_to_file(data: Dict[str, Any], filename: str):
    """
    Logs data to a specified file in JSON format.

    Args:
        data (Dict[str, Any]): The data to log.
        filename (str): The name of the file to log the data to.
    """
    with open(filename, 'a') as f:
        f.write(json.dumps(data) + '\n')

def load_from_file(filename: str) -> List[Dict[str, Any]]:
    """
    Loads data from a specified file in JSON format.

    Args:
        filename (str): The name of the file to load data from.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the loaded data.
    """
    data = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                data.append(json.loads(line.strip()))
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {filename}.")
    return data
