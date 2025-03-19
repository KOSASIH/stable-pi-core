# ggf/__init__.py

"""
Galactic Governance Framework (GGF) Package
This package provides a framework for decentralized governance across planets and star systems.
"""

__version__ = "2.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import necessary components
from .voting_system import VotingSystem
from .decision_engine import DecisionEngine
from .smart_contracts import SmartContracts
from .communication import Communication
from .config import Config

# Initialize logging
import logging
import sys

def setup_logging():
    """Set up logging for the GGF package with advanced configuration."""
    logging_level = Config.DEFAULTS["LOGGING_LEVEL"]
    logging_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(level=logging_level, format=logging_format, stream=sys.stdout)
    logging.info("GGF package logging initialized.")
    logging.debug("Debugging mode is enabled.")

# Call the setup_logging function to initialize logging
setup_logging()

def initialize_ggf():
    """Initialize the GGF system components."""
    logging.info("Initializing GGF system components.")
    voting_system = VotingSystem()
    decision_engine = DecisionEngine()
    smart_contracts = SmartContracts()
    communication = Communication()
    logging.info("GGF system components initialized successfully.")
    return voting_system, decision_engine, smart_contracts, communication

# Initialize the GGF system components when the module is imported
voting_system, decision_engine, smart_contracts, communication = initialize_ggf()

__all__ = [
    "VotingSystem",
    "DecisionEngine",
    "SmartContracts",
    "Communication",
    "Config",
    "voting_system",
    "decision_engine",
    "smart_contracts",
    "communication"
]
