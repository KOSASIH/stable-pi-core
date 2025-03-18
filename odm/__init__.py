"""
Orbital Data Marketplace (ODM) Package

This package provides functionalities for the Orbital Data Marketplace,
allowing users to buy and sell space-based data using smart contracts and
tokenized transactions.

Modules:
- contracts: Contains smart contracts for managing data listings and transactions.
- data: Handles data management and analysis.
- nodes: Implements the space-based node network for data collection.
- user_interface: Provides the user interface for the marketplace.
- tests: Contains unit tests for the ODM components.
- config: Configuration settings for the ODM feature.
- utils: Utility functions for common tasks within the ODM package.
"""

# Import necessary modules for easy access
from .contracts import orbital_data_marketplace
from .data import data_manager, data_analysis
from .nodes import node, node_network
from .user_interface import app
from .config import Config
from .utils import log_info, log_error

# Package version (optional)
__version__ = "0.1.0"

# Initialize any necessary components or configurations
def initialize_odm():
    """
    Initialize the ODM package.
    This function can be used to set up any necessary configurations or
    connections required for the ODM to function properly.
    """
    log_info("Initializing Orbital Data Marketplace (ODM)...")
    # Additional initialization logic can be added here
