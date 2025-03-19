# pqpn/__init__.py

"""
Photonic Quantum Processor Network (PQPN) Package

This package implements the Photonic Quantum Processor Network feature,
which includes functionalities for managing photonic quantum processors,
data transmission, and quantum AI integration.
"""

# Import necessary classes and functions for PQPN
from .pqpn_manager import PQPNManager
from .photonic_processor import PhotonicProcessor
from .data_transmission import PhotonicDataTransmission
from .quantum_ai import QuantumAI
from .utils import load_config, save_to_file

__all__ = [
    "PQPNManager",
    "PhotonicProcessor",
    "PhotonicDataTransmission",
    "QuantumAI",
    "load_config",
    "save_to_file"
]

# Load configuration for PQPN
config = load_config("pqpn/pqpn_config.yaml")

# Initialize the PQPN Manager with the loaded configuration
pqpn_manager = PQPNManager(config)

def start_pqpn():
    """
    Start the Photonic Quantum Processor Network.

    This function initializes the PQPN and begins processing tasks.
    """
    pqpn_manager.initialize_processors()
    pqpn_manager.start_data_transmission()
    pqpn_manager.run_quantum_ai_tasks()

    print("Photonic Quantum Processor Network is up and running.")

# If this module is run directly, start the PQPN
if __name__ == "__main__":
    start_pqpn()
