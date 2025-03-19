# biosensors/data_processing.py

import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataProcessor:
    def __init__(self):
        """
        Initialize the DataProcessor.
        """
        self.processed_data = {}

    def validate_data(self, raw_data):
        """
        Validate the raw data from biosensors.
        
        :param raw_data: Dictionary containing raw data from sensors.
        :return: Boolean indicating whether the data is valid.
        """
        for sensor_id, data in raw_data.items():
            if not isinstance(data, dict):
                logging.warning(f"Invalid data format for sensor {sensor_id}. Expected a dictionary.")
                return False
            
            if 'temperature' not in data or 'heart_rate' not in data:
                logging.warning(f"Missing required fields in data from sensor {sensor_id}.")
                return False
            
            if not (30 <= data['temperature'] <= 45):  # Example temperature range in Celsius
                logging.warning(f"Temperature out of range for sensor {sensor_id}: {data['temperature']}")
                return False
            
            if not (40 <= data['heart_rate'] <= 180):  # Example heart rate range in BPM
                logging.warning(f"Heart rate out of range for sensor {sensor_id}: {data['heart_rate']}")
                return False
        
        return True

    def normalize_data(self, raw_data):
        """
        Normalize the raw data for further analysis.
        
        :param raw_data: Dictionary containing raw data from sensors.
        :return: Dictionary containing normalized data.
        """
        normalized_data = {}
        for sensor_id, data in raw_data.items():
            normalized_data[sensor_id] = {
                "temperature": self._normalize(data['temperature'], 30, 45),  # Normalize temperature
                "heart_rate": self._normalize(data['heart_rate'], 40, 180)   # Normalize heart rate
            }
        return normalized_data

    def _normalize(self, value, min_value, max_value):
        """
        Normalize a value to a range of 0 to 1.
        
        :param value: The value to normalize.
        :param min_value: The minimum value of the range.
        :param max_value: The maximum value of the range.
        :return: Normalized value.
        """
        return (value - min_value) / (max_value - min_value)

    def analyze_data(self, normalized_data):
        """
        Perform basic statistical analysis on the normalized data.
        
        :param normalized_data: Dictionary containing normalized data from sensors.
        :return: Dictionary containing statistical analysis results.
        """
        analysis_results = {}
        for sensor_id, data in normalized_data.items():
            analysis_results[sensor_id] = {
                "temperature_mean": np.mean(data['temperature']),
                "heart_rate_mean": np.mean(data['heart_rate']),
                "temperature_std": np.std(data['temperature']),
                "heart_rate_std": np.std(data['heart_rate'])
            }
        return analysis_results

if __name__ == "__main__":
    # Example usage
    raw_data = {
        "sensor_1": {"temperature": 36.5, "heart_rate": 75},
        "sensor_2": {"temperature": 37.0, "heart_rate": 80},
        "sensor_3": {"temperature": 38.2, "heart_rate": 90}
    }

    processor = DataProcessor()

    if processor.validate_data(raw_data):
        normalized_data = processor.normalize_data(raw_data)
        analysis_results = processor.analyze_data(normalized_data)
        print("Normalized Data:", normalized_data)
        print("Analysis Results:", analysis_results)
    else:
        logging.error("Raw data validation failed.")
