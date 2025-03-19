# dmec/main.py

import threading
import time
import logging
from detector import DarkMatterDetector
from energy_converter import EnergyConverter
from data_handler import DataHandler
from communication import Communication
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG if Config.LOGGING_ENABLED else logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class DMECSystem:
    def __init__(self):
        self.detector = DarkMatterDetector()
        self.converter = EnergyConverter()
        self.data_handler = DataHandler()
        self.communication = Communication()
        self.running = True

    def start_detection(self):
        """Thread for running the dark matter detection."""
        while self.running:
            interaction = self.detector.detect_interaction()
            if interaction:
                energy = self.converter.convert(Config.ENERGY_PER_INTERACTION)
                logging.info(f"Interaction detected! Total Energy Output: {energy} units")
                self.data_handler.save_data(energy)
                self.communication.publish(Config.MQTT_TOPIC, energy)
            time.sleep(Config.DETECTION_INTERVAL)

    def run(self):
        """Start the DMEC system."""
        self.communication.start()
        detection_thread = threading.Thread(target=self.start_detection)
        detection_thread.start()

        try:
            while self.running:
                time.sleep(1)  # Main thread can perform other tasks or just wait
        except KeyboardInterrupt:
            logging.info("Shutting down DMEC...")
            self.running = False
        finally:
            detection_thread.join()
            self.communication.client.loop_stop()
            logging.info("DMEC system stopped.")

if __name__ == "__main__":
    dmc_system = DMECSystem()
    dmc_system.run()
