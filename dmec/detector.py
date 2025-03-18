# dmec/detector.py

import random
import time
from .config import Config

class DarkMatterDetector:
    def __init__(self):
        self.energy_output = 0

    def detect_interaction(self):
        # Simulate dark matter interaction detection based on sensitivity
        interaction = random.random() < Config.DETECTOR_SENSITIVITY
        return interaction

    def run(self):
        while True:
            interaction = self.detect_interaction()
            if interaction:
                self.energy_output += Config.ENERGY_PER_INTERACTION
                print(f"Interaction detected! Current energy output: {self.energy_output} units")
            time.sleep(Config.DETECTION_INTERVAL)
