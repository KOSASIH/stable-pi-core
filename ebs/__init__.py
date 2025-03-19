# ebs/__init__.py

"""
Exo-Blockchain Synchronization (EBS) Package
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .signal_detector import SignalDetector
from .blockchain_sync import BlockchainSync
from .ai_security import AISecurity
from .config import Config

# Initialize logging
import logging

def setup_logging():
    """Set up logging for the EBS package."""
    logging.basicConfig(
        level=Config.DEFAULTS["LOGGING_LEVEL"],
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("EBS package logging initialized.")

# Call the setup_logging function to initialize logging
setup_logging()

__all__ = [
    "SignalDetector",
    "BlockchainSync",
    "AISecurity",
    "Config"
]
