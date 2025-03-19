# core/quantum_gravity_sensor.py

import logging
import numpy as np
import random
import time

# Configure logging for Quantum Gravity Sensor
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuantumGravitySensor:
    """
    Represents a quantum gravity sensor that measures gravitational fields.
    """

    def __init__(self, sensor_id, calibration_factor=1.0):
        """
        Initialize the Quantum Gravity Sensor.

        :param sensor_id: Unique identifier for the sensor.
        :param calibration_factor: Calibration factor for the sensor.
        """
        self.sensor_id = sensor_id
        self.calibration_factor = calibration_factor
        self.measurements = []
        logger.info("Quantum Gravity Sensor %s initialized with calibration factor: %.2f", self.sensor_id, self.calibration_factor)

    def measure_gravity(self):
        """
        Simulate a gravity measurement.

        :return: Measured gravity value (in m/s^2).
        """
        # Simulate a random gravity measurement with some noise
        base_gravity = 9.81  # Standard gravity in m/s^2
        noise = random.uniform(-0.05, 0.05)  # Simulated noise
        measured_gravity = (base_gravity + noise) * self.calibration_factor
        self.measurements.append(measured_gravity)
        logger.info("Sensor %s measured gravity: %.4f m/s^2", self.sensor_id, measured_gravity)
        return measured_gravity

    def calibrate(self, new_calibration_factor):
        """
        Calibrate the sensor with a new calibration factor.

        :param new_calibration_factor: New calibration factor for the sensor.
        """
        self.calibration_factor = new_calibration_factor
        logger.info("Sensor %s calibrated with new factor: %.2f", self.sensor_id, self.calibration_factor)

    def get_average_measurement(self):
        """
        Get the average of all measurements taken by the sensor.

        :return: Average gravity measurement.
        """
        if not self.measurements:
            logger.warning("No measurements available to calculate average.")
            return None
        average = np.mean(self.measurements)
        logger.info("Sensor %s average gravity measurement: %.4f m/s^2", self.sensor_id, average)
        return average

    def reset_measurements(self):
        """
        Reset the measurements recorded by the sensor.
        """
        self.measurements.clear()
        logger.info("Sensor %s measurements reset.", self.sensor_id)

    def simulate_measurements(self, num_measurements, interval=1):
        """
        Simulate multiple gravity measurements over a specified interval.

        :param num_measurements: Number of measurements to simulate.
        :param interval: Time interval (in seconds) between measurements.
        """
        logger.info("Starting simulation of %d measurements with %.1f seconds interval.", num_measurements, interval)
        for _ in range(num_measurements):
            self.measure_gravity()
            time.sleep(interval)
        logger.info("Simulation complete.")

# Example usage
if __name__ == "__main__":
    # Create a quantum gravity sensor
    sensor = QuantumGravitySensor(sensor_id="QGS-001")

    # Perform measurements
    sensor.simulate_measurements(num_measurements=5, interval=1)

    # Get average measurement
    average_measurement = sensor.get_average_measurement()
    print(f"Average gravity measurement: {average_measurement:.4f} m/s^2")

    # Calibrate the sensor
    sensor.calibrate(new_calibration_factor=1.02)

    # Perform another measurement after calibration
    sensor.measure_gravity()

    # Reset measurements
    sensor.reset_measurements()
