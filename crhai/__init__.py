# crhai/__init__.py

"""
Cosmic Radiation Hardened AI (CRHAI) Package
This package provides advanced AI capabilities designed to operate in cosmic radiation environments.
"""

__version__ = "2.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import necessary components
from .radiation_hardened_ai import RadiationHardenedAI
from .edge_computing import EdgeComputing
from .config import Config

# Initialize logging
import logging
import sys

def setup_logging():
    """Set up logging for the CRHAI package with advanced configuration."""
    logging_level = Config.DEFAULTS["LOGGING_LEVEL"]
    logging_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(level=logging_level, format=logging_format, stream=sys.stdout)
    logging.info("CRHAI package logging initialized.")
    logging.debug("Debugging mode is enabled.")

# Call the setup_logging function to initialize logging
setup_logging()

def initialize_crhai():
    """Initialize the CRHAI system components."""
    logging.info("Initializing CRHAI system components.")
    ai_system = RadiationHardenedAI(model_count=Config.DEFAULTS["MODEL_COUNT"])
    edge_computer = EdgeComputing()
    logging.info("CRHAI system components initialized successfully.")
    return ai_system, edge_computer

# Initialize the CRHAI system components when the module is imported
ai_system, edge_computer = initialize_crhai()

__all__ = [
    "RadiationHardenedAI",
    "EdgeComputing",
    "Config",
    "ai_system",
    "edge_computer"
    ]
