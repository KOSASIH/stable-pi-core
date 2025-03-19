# pqpn/pqpn_manager.py

import logging
import time
from .photonic_processor import PhotonicProcessor
from .data_transmission import PhotonicDataTransmission
from .quantum_ai import QuantumAI
from .utils import load_config

# Configure logging for PQPN Manager
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PQPNManager:
    """
    Manages interactions between components of the Photonic Quantum Processor Network (PQPN).
    """

    def __init__(self, config):
        """
        Initialize the PQPN Manager.

        :param config: Configuration dictionary for PQPN settings.
        """
        self.config = config
        self.processors = []
        self.data_transmission = PhotonicDataTransmission(config['data_transmission'])
        self.quantum_ai = QuantumAI(config['quantum_ai'])

        # Initialize photonic processors
        self.initialize_processors()

    def initialize_processors(self):
        """
        Initialize photonic processors based on the configuration.
        """
        max_processors = self.config['photonic_processor']['max_processors']
        processor_type = self.config['photonic_processor']['processor_type']

        for i in range(max_processors):
            try:
                processor = PhotonicProcessor(processor_type, i)
                self.processors.append(processor)
                logger.info(f"Initialized {processor_type} processor {i}.")
            except Exception as e:
                logger.error(f"Failed to initialize processor {i}: {e}")

    def start_data_transmission(self):
        """
        Start the data transmission process.
        """
        try:
            logger.info("Starting data transmission...")
            self.data_transmission.start()
            logger.info("Data transmission started successfully.")
        except Exception as e:
            logger.error(f"Error starting data transmission: {e}")

    def run_quantum_ai_tasks(self):
        """
        Run quantum AI tasks using the initialized processors.
        """
        logger.info("Running Quantum AI tasks...")
        for processor in self.processors:
            try:
                result = self.quantum_ai.process_data(processor)
                logger.info(f"Processor {processor.id} completed Quantum AI task with result: {result}")
            except Exception as e:
                logger.error(f"Error processing data with processor {processor.id}: {e}")

    def shutdown(self):
        """
        Shutdown the PQPN, stopping all processes and cleaning up resources.
        """
        logger.info("Shutting down PQPN...")
        try:
            self.data_transmission.stop()
            logger.info("Data transmission stopped.")
            for processor in self.processors:
                processor.shutdown()
                logger.info(f"Processor {processor.id} has been shut down.")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

# Example usage
if __name__ == "__main__":
    try:
        config = load_config("pqpn/pqpn_config.yaml")
        pqpn_manager = PQPNManager(config)

        pqpn_manager.start_data_transmission()
        pqpn_manager.run_quantum_ai_tasks()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        pqpn_manager.shutdown()
