# nbca/__init__.py

"""
Neutrino-Based Communication Array (NBCA) Package
"""

__version__ = "2.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import necessary components
from .neutrino_detector import NeutrinoDetector
from .quantum_processor import QuantumProcessor
from .communication_protocol import CommunicationProtocol
from .data_processing import DataProcessing
from .config import Config

# Initialize logging
import logging
import sys

def setup_logging():
    """Set up logging for the NBCA package with advanced configuration."""
    logging_level = Config.DEFAULTS["LOGGING_LEVEL"]
    logging_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(level=logging_level, format=logging_format, stream=sys.stdout)
    logging.info("NBCA package logging initialized.")
    logging.debug("Debugging mode is enabled.")

# Call the setup_logging function to initialize logging
setup_logging()

__all__ = [
    "NeutrinoDetector",
    "QuantumProcessor",
    "CommunicationProtocol",
    "DataProcessing",
    "Config"
]
