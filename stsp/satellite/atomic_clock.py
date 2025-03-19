# stsp/satellite/atomic_clock.py

import logging
import time
import random

class AtomicClock:
    """
    Represents an atomic clock for precise timekeeping.
    """

    def __init__(self):
        """
        Initialize the AtomicClock instance.
        """
        self.current_time = self.get_current_time()
        logging.info("AtomicClock initialized with current time: %s", self.current_time)

    def get_current_time(self):
        """
        Retrieve the current time from the atomic clock.
        
        :return: The current time as a timestamp.
        """
        # Simulate retrieving time from an atomic clock
        self.current_time = time.time()  # Use system time for simulation
        logging.info("Current time retrieved from atomic clock: %s", self.current_time)
        return self.current_time

    def synchronize_with_external_source(self, external_time):
        """
        Synchronize the atomic clock with an external time source.
        
        :param external_time: The external time to synchronize with.
        """
        logging.info("Synchronizing atomic clock with external time: %s", external_time)
        self.current_time = external_time
        logging.info("Atomic clock synchronized. New time: %s", self.current_time)

    def simulate_clock_drift(self, drift_rate=0.0001):
        """
        Simulate clock drift over time.
        
        :param drift_rate: The rate of drift per second (default is 0.0001 seconds).
        :return: The adjusted current time after drift.
        """
        drift = random.uniform(-drift_rate, drift_rate)
        self.current_time += drift
        logging.info("Simulated clock drift. New time: %s", self.current_time)
        return self.current_time

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    atomic_clock = AtomicClock()

    # Retrieve current time
    current_time = atomic_clock.get_current_time()
    print(f"Current Atomic Clock Time: {current_time}")

    # Synchronize with an external time source
    external_time = time.time() + 3600  # Simulate an external time (1 hour ahead)
    atomic_clock.synchronize_with_external_source(external_time)

    # Simulate clock drift
    adjusted_time = atomic_clock.simulate_clock_drift()
    print(f"Adjusted Atomic Clock Time after Drift: {adjusted_time}")
