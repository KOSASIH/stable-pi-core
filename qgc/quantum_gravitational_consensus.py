# qgc/quantum_gravitational_consensus.py

import logging
import numpy as np

class QuantumGravitationalConsensus:
    """
    Implements the consensus algorithm based on gravitational measurements
    from multiple nodes in the Quantum Gravitational Consensus (QGC) system.
    """

    def __init__(self, initial_threshold=0.1, adjustment_factor=0.05):
        """
        Initialize the consensus algorithm.

        :param initial_threshold: The initial acceptable deviation threshold for consensus.
        :param adjustment_factor: The factor by which to adjust the threshold based on measurement variability.
        """
        self.measurements = []
        self.threshold = initial_threshold
        self.adjustment_factor = adjustment_factor
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def add_measurement(self, measurement):
        """
        Add a gravitational measurement to the consensus pool.

        :param measurement: The gravitational measurement to add.
        """
        self.measurements.append(measurement)
        self.logger.info(f"Measurement added: {measurement:.4f} m/s^2")

    def adjust_threshold(self):
        """
        Adjust the threshold based on the variability of the measurements.
        """
        if len(self.measurements) < 2:
            return  # Not enough data to adjust

        std_dev = np.std(self.measurements)
        self.threshold = min(max(std_dev * self.adjustment_factor, 0.01), 0.5)  # Keep threshold within reasonable bounds
        self.logger.info(f"Threshold adjusted to: {self.threshold:.4f} m/s^2")

    def reach_consensus(self):
        """
        Reach consensus based on the collected measurements.

        :return: The consensus value if reached, otherwise None.
        """
        if not self.measurements:
            self.logger.warning("No measurements available to reach consensus.")
            return None

        # Calculate the mean and standard deviation of the measurements
        mean_measurement = np.mean(self.measurements)
        std_dev = np.std(self.measurements)

        # Filter out measurements that deviate too much from the mean
        filtered_measurements = [
            m for m in self.measurements 
            if abs(m - mean_measurement) <= self.threshold * std_dev
        ]

        if not filtered_measurements:
            self.logger.warning("No valid measurements to reach consensus.")
            return None

        consensus_value = np.mean(filtered_measurements)
        self.logger.info(f"Consensus reached: {consensus_value:.4f} m/s^2 based on {len(filtered_measurements)} valid measurements.")
        
        # Clear measurements after reaching consensus
        self.measurements.clear()
        return consensus_value

    def reset(self):
        """
        Reset the consensus pool.
        """
        self.measurements.clear()
        self.logger.info("Consensus pool has been reset.")

    def get_measurement_statistics(self):
        """
        Get statistics of the current measurements.

        :return: A dictionary containing mean and standard deviation of measurements.
        """
        if not self.measurements:
            return {"mean": None, "std_dev": None}

        mean = np.mean(self.measurements)
        std_dev = np.std(self.measurements)
        return {"mean": mean, "std_dev": std_dev}

# Example usage
if __name__ == "__main__":
    consensus = QuantumGravitationalConsensus(initial_threshold=0.1, adjustment_factor=0.05)

    # Simulate adding measurements
    simulated_measurements = [9.80, 9.81, 9.79, 9.82, 9.75, 9.85, 9.78, 9.90]  # Example measurements
    for measurement in simulated_measurements:
        consensus.add_measurement(measurement)

    # Adjust threshold based on measurements
    consensus.adjust_threshold()

    # Reach consensus
    consensus_value = consensus.reach_consensus()
    print(f"Consensus Value: {consensus_value:.4f} m/s^2")

    # Get measurement statistics
    stats = consensus.get_measurement_statistics()
    print(f"Measurement Statistics: Mean = {stats['mean']:.4f}, Std Dev = {stats['std_dev']:.4f}")
