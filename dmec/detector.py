# dmec/detector.py

import random
import time
import logging
from .config import Config

class DarkMatterDetector:
    def __init__(self):
        self.energy_output = 0
        self.sensitivity = Config.DEFAULTS["DETECTOR_SENSITIVITY"]
        logging.info(f"Dark Matter Detector initialized with sensitivity: {self.sensitivity}")

    def detect_interaction(self):
        """
        Simulate dark matter interaction detection based on sensitivity.
        Returns True if an interaction is detected, otherwise False.
        """
        interaction = random.random() < self.sensitivity
        if interaction:
            logging.debug("Dark matter interaction detected.")
        return interaction

    def run(self):
        """
        Continuously run the detection process.
        This method can be run in a separate thread.
        """
        logging.info("Starting detection process...")
        while True:
            interaction = self.detect_interaction()
            if interaction:
                self.energy_output += Config.DEFAULTS["ENERGY_PER_INTERACTION"]
                logging.info(f"Interaction detected! Current energy output: {self.energy_output} units")
            time.sleep(Config.DEFAULTS["DETECTION_INTERVAL"])

    def set_sensitivity(self, new_sensitivity):
        """
        Set a new sensitivity for the detector.
        Ensures the sensitivity is within valid bounds.
        """
        if 0 <= new_sensitivity <= 1:
            self.sensitivity = new_sensitivity
            logging.info(f"Detector sensitivity updated to: {self.sensitivity}")
        else:
            logging.error("Sensitivity must be between 0 and 1.")
            raise ValueError("Sensitivity must be between 0 and 1.")

    def get_energy_output(self):
        """
        Return the current energy output.
        """
        return self.energy_output
