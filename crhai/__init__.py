# crhai/__init__.py

"""
Cosmic Radiation Hardened AI (CRHAI) Package
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import necessary components
from .radiation_hardened_ai import RadiationHardenedAI
from .edge_computing import EdgeComputing
from .config import Config

# Initialize logging
import logging

def setup_logging():
    """Set up logging for the CRHAI package."""
    logging.basicConfig(
        level=Config.DEFAULTS["LOGGING_LEVEL"],
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("CRHAI package logging initialized.")

# Call the setup_logging function to initialize logging
setup_logging()

__all__ = [
    "RadiationHardenedAI",
    "EdgeComputing",
    "Config"
]
