# nbca/neutrino_detector.py

import logging
import random
import time

class NeutrinoDetector:
    def __init__(self, detector_type="IceCube"):
        """
        Initialize the Neutrino Detector.
        :param detector_type: The type of neutrino detector (e.g., IceCube, Super-Kamiokande).
        """
        self.detector_type = detector_type
        self.detection_threshold = 0.1  # Default threshold for neutrino detection
        self.is_operational = True
        logging.info(f"{self.detector_type} Neutrino Detector initialized and operational.")

    def set_detection_threshold(self, threshold):
        """
        Set the detection threshold for neutrino events.
        :param threshold: Probability threshold for detecting a neutrino event (0 to 1).
        """
        if 0 <= threshold <= 1:
            self.detection_threshold = threshold
            logging.info(f"Detection threshold set to {self.detection_threshold}.")
        else:
            logging.error("Threshold must be between 0 and 1.")
            raise ValueError("Threshold must be between 0 and 1.")

    def detect_event(self):
        """
        Simulate the detection of a neutrino event.
        :return: A simulated event or None if no event is detected.
        """
        if not self.is_operational:
            logging.warning("Detector is not operational.")
            return None

        # Simulate a random chance of detecting a neutrino event based on the threshold
        detection_probability = random.random()
        logging.debug(f"Detection probability: {detection_probability}, Threshold: {self.detection_threshold}")

        if detection_probability < self.detection_threshold:
            event = {
                "event_id": self.generate_event_id(),
                "timestamp": time.time(),
                "energy": random.uniform(1e-6, 1e-2),  # Simulated energy in GeV
                "direction": self.generate_random_direction()
            }
            logging.info(f"Neutrino event detected: {event}")
            return event
        else:
            logging.info("No neutrino event detected.")
            return None

    def generate_event_id(self):
        """Generate a unique event ID."""
        return f"NEUTRINO-{int(time.time() * 1000)}-{random.randint(1000, 9999)}"

    def generate_random_direction(self):
        """Generate a random direction for the neutrino event."""
        # Randomly generate spherical coordinates (theta, phi)
        theta = random.uniform(0, 3.14159)  # Polar angle
        phi = random.uniform(0, 2 * 3.14159)  # Azimuthal angle
        return {
            "theta": theta,
            "phi": phi
        }

    def operational_status(self):
        """Check the operational status of the detector."""
        return self.is_operational

    def shutdown(self):
        """Shut down the detector."""
        self.is_operational = False
        logging.info(f"{self.detector_type} Neutrino Detector has been shut down.")

    def restart(self):
        """Restart the detector."""
        self.is_operational = True
        logging.info(f"{self.detector_type} Neutrino Detector has been restarted.")
