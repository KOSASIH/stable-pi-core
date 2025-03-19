# bqpl/biosensor.py

import random
import logging

class Biosensor:
    """
    Represents a biosensor for collecting biological data.
    """

    def __init__(self, sensor_id):
        """
        Initialize the biosensor.

        :param sensor_id: Unique identifier for the biosensor.
        """
        self.sensor_id = sensor_id
        logging.basicConfig(level=logging.INFO)

    def read_data(self):
        """
        Simulate reading biological data from the sensor.

        :return: A simulated biological data reading (e.g., heart rate, temperature).
        """
        # Simulate biological data collection
        heart_rate = random.randint(60, 100)  # Simulated heart rate in beats per minute
        temperature = round(random.uniform(36.0, 38.5), 2)  # Simulated body temperature in Celsius

        # Create a data dictionary
        data = {
            "heart_rate": heart_rate,
            "temperature": temperature
        }

        logging.info(f"Biosensor {self.sensor_id}: Collected data: {data}")
        return data

# Example usage
if __name__ == "__main__":
    # Create a biosensor instance
    biosensor = Biosensor(sensor_id="Biosensor_1")

    # Read data from the biosensor
    collected_data = biosensor.read_data()
    print(f"Collected Biological Data: {collected_data}")
