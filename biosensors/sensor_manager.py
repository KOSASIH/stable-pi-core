# biosensors/sensor_manager.py

import time
import random
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SensorManager:
    def __init__(self, sensor_ids):
        """
        Initialize the SensorManager with a list of sensor IDs.
        
        :param sensor_ids: List of sensor IDs to manage.
        """
        self.sensor_ids = sensor_ids
        self.connected_sensors = {}
        self.data = {}

    def connect_sensors(self):
        """
        Connect to the biosensors and store their connection status.
        """
        for sensor_id in self.sensor_ids:
            try:
                # Simulate connecting to a sensor (replace with actual connection logic)
                self.connected_sensors[sensor_id] = True
                logging.info(f"Connected to sensor {sensor_id}.")
            except Exception as e:
                logging.error(f"Failed to connect to sensor {sensor_id}: {e}")

    def collect_data(self):
        """
        Collect data from connected biosensors.
        
        :return: A dictionary containing sensor data.
        """
        for sensor_id in self.connected_sensors:
            if self.connected_sensors[sensor_id]:
                try:
                    # Simulate data collection (replace with actual data retrieval logic)
                    sensor_data = self._simulate_data_collection(sensor_id)
                    self.data[sensor_id] = sensor_data
                    logging.info(f"Collected data from sensor {sensor_id}: {sensor_data}")
                except Exception as e:
                    logging.error(f"Failed to collect data from sensor {sensor_id}: {e}")
        return self.data

    def _simulate_data_collection(self, sensor_id):
        """
        Simulate data collection from a sensor.
        
        :param sensor_id: The ID of the sensor to collect data from.
        :return: Simulated sensor data.
        """
        # Simulate different types of data (e.g., temperature, heart rate)
        return {
            "temperature": round(random.uniform(36.0, 38.5), 2),  # Simulated temperature in Celsius
            "heart_rate": random.randint(60, 100),               # Simulated heart rate in BPM
            "timestamp": time.time()                               # Current timestamp
        }

    def disconnect_sensors(self):
        """
        Disconnect from all biosensors.
        """
        for sensor_id in self.connected_sensors:
            if self.connected_sensors[sensor_id]:
                # Simulate disconnecting from a sensor (replace with actual disconnection logic)
                self.connected_sensors[sensor_id] = False
                logging.info(f"Disconnected from sensor {sensor_id}.")

if __name__ == "__main__":
    # Example usage
    sensor_ids = ["sensor_1", "sensor_2", "sensor_3"]
    manager = SensorManager(sensor_ids)

    manager.connect_sensors()
    collected_data = manager.collect_data()
    print(json.dumps(collected_data, indent=4))
    manager.disconnect_sensors()
