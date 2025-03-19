# biosensors/utils.py

import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def format_sensor_data(sensor_id, data):
    """
    Format the sensor data into a readable string.
    
    :param sensor_id: The ID of the sensor.
    :param data: Dictionary containing sensor data.
    :return: Formatted string representation of the sensor data.
    """
    try:
        formatted_data = f"Sensor ID: {sensor_id}\n"
        formatted_data += f"Temperature: {data['temperature']} °C\n"
        formatted_data += f"Heart Rate: {data['heart_rate']} BPM\n"
        formatted_data += f"Timestamp: {format_timestamp(data['timestamp'])}\n"
        return formatted_data
    except KeyError as e:
        logging.error(f"Missing key in data for sensor {sensor_id}: {e}")
        return None

def format_timestamp(timestamp):
    """
    Convert a timestamp to a human-readable format.
    
    :param timestamp: The timestamp to format.
    :return: Formatted timestamp string.
    """
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def log_error(message):
    """
    Log an error message.
    
    :param message: The error message to log.
    """
    logging.error(message)

def log_info(message):
    """
    Log an informational message.
    
    :param message: The informational message to log.
    """
    logging.info(message)

def calculate_average(data_list):
    """
    Calculate the average of a list of numerical values.
    
    :param data_list: List of numerical values.
    :return: Average value.
    """
    if not data_list:
        logging.warning("Empty data list provided for average calculation.")
        return None
    return sum(data_list) / len(data_list)

def calculate_standard_deviation(data_list):
    """
    Calculate the standard deviation of a list of numerical values.
    
    :param data_list: List of numerical values.
    :return: Standard deviation value.
    """
    if not data_list:
        logging.warning("Empty data list provided for standard deviation calculation.")
        return None
    mean = calculate_average(data_list)
    variance = sum((x - mean) ** 2 for x in data_list) / len(data_list)
    return variance ** 0.5

if __name__ == "__main__":
    # Example usage
    sensor_id = "sensor_1"
    sensor_data = {
        "temperature": 36.5,
        "heart_rate": 75,
        "timestamp": 1633072800  # Example timestamp
    }

    formatted_data = format_sensor_data(sensor_id, sensor_data)
    if formatted_data:
        print(formatted_data)

    average_temp = calculate_average([36.5, 37.0, 38.2])
    print(f"Average Temperature: {average_temp} °C")

    std_dev_hr = calculate_standard_deviation([75, 80, 90])
    print(f"Standard Deviation of Heart Rate: {std_dev_hr} BPM")
