# hql/__init__.py

"""
Holographic Quantum Ledger (HQL) Package
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .holographic_ledger import HolographicQuantumLedger
from .quantum_interference import QuantumInterference
from .config import Config

# Initialize logging
import logging

def setup_logging():
    """Set up logging for the HQL package."""
    logging.basicConfig(
        level=Config.DEFAULTS["LOGGING_LEVEL"],
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("HQL package logging initialized.")

# Call the setup_logging function to initialize logging
setup_logging()

__all__ = [
    "HolographicQuantumLedger",
    "QuantumInterference",
    "Config"
]
