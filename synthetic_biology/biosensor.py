import random
import time
import json
from typing import Any, Dict

class Biosensor:
    """
    A class to represent a biosensor.

    Attributes:
        sensor_id (str): Unique identifier for the biosensor.
        sensor_type (str): Type of the biosensor (e.g., DNA, glucose).
        data (Dict[str, Any]): Latest data collected by the biosensor.
        is_active (bool): Status of the biosensor (active/inactive).
    """

    def __init__(self, sensor_id: str, sensor_type: str):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.data = {}
        self.is_active = True

    def collect_data(self) -> Dict[str, Any]:
        """
        Simulates data collection from the biosensor.

        Returns:
            Dict[str, Any]: A dictionary containing the collected data.
        """
        if not self.is_active:
            raise Exception(f"Biosensor {self.sensor_id} is inactive.")

        # Simulate data collection (replace with actual sensor data collection logic)
        self.data = {
            "timestamp": time.time(),
            "value": random.uniform(0, 100),  # Simulated sensor value
            "unit": "units"  # Replace with actual unit of measurement
        }
        return self.data

    def deactivate(self):
        """Deactivates the biosensor."""
        self.is_active = False

    def activate(self):
        """Activates the biosensor."""
        self.is_active = True

    def get_status(self) -> str:
        """Returns the status of the biosensor."""
        return "Active" if self.is_active else "Inactive"

    def to_json(self) -> str:
        """Converts the biosensor data to JSON format."""
        return json.dumps({
            "sensor_id": self.sensor_id,
            "sensor_type": self.sensor_type,
            "data": self.data,
            "is_active": self.is_active
        })


class BiosensorManager:
    """
    A class to manage multiple biosensors.

    Attributes:
        biosensors (Dict[str, Biosensor]): A dictionary of biosensors managed by this manager.
    """

    def __init__(self):
        self.biosensors = {}

    def add_biosensor(self, biosensor: Biosensor):
        """Adds a biosensor to the manager."""
        self.biosensors[biosensor.sensor_id] = biosensor

    def remove_biosensor(self, sensor_id: str):
        """Removes a biosensor from the manager."""
        if sensor_id in self.biosensors:
            del self.biosensors[sensor_id]

    def collect_data_from_all(self) -> Dict[str, Dict[str, Any]]:
        """
        Collects data from all managed biosensors.

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary containing data from all biosensors.
        """
        collected_data = {}
        for sensor_id, biosensor in self.biosensors.items():
            try:
                collected_data[sensor_id] = biosensor.collect_data()
            except Exception as e:
                collected_data[sensor_id] = {"error": str(e)}
        return collected_data

    def get_biosensor_status(self) -> Dict[str, str]:
        """Returns the status of all managed biosensors."""
        return {sensor_id: biosensor.get_status() for sensor_id, biosensor in self.biosensors.items()}

    def to_json(self) -> str:
        """Converts the biosensor manager data to JSON format."""
        return json.dumps({
            "biosensors": {sensor_id: biosensor.to_json() for sensor_id, biosensor in self.biosensors.items()}
        })
