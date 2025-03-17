"""
Synthetic Biology Module for Stable Pi Core

This module provides an interface for interacting with synthetic biology systems,
including IoT-based biosensors, edge computing functionalities, and blockchain
integration for data logging.

Modules:
- biosensor: Classes and functions for managing biosensors.
- edge_computing: Functions for processing data at the edge.
- data_logging: Functions for logging biosensor data to the blockchain.
- smart_contracts: Smart contracts for handling biosensor data.
- utils: Utility functions for the synthetic biology interface.
"""

from .biosensor import Biosensor, BiosensorManager
from .edge_computing import EdgeProcessor
from .data_logging import log_data_to_blockchain
from .smart_contracts import SmartContractManager
from .utils import format_sensor_data, validate_sensor_data

__all__ = [
    "Biosensor",
    "BiosensorManager",
    "EdgeProcessor",
    "log_data_to_blockchain",
    "SmartContractManager",
    "format_sensor_data",
    "validate_sensor_data",
]

# Initialize the synthetic biology module
def initialize_synthetic_biology():
    """
    Initializes the synthetic biology module.
    This function can be called to set up any necessary configurations
    or connections required for the module to function properly.
    """
    print("Initializing Synthetic Biology Module...")
    # Add any initialization logic here, such as connecting to databases
    # or setting up communication with IoT devices.
    # For example:
    # BiosensorManager.initialize()
    # EdgeProcessor.initialize()
    # SmartContractManager.initialize()
    print("Synthetic Biology Module initialized successfully.")
