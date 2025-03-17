"""
edge_computing - A module for edge computing in photonic data transmission systems.

This module provides classes and functions for managing edge nodes
and processing data at the edge of the network.

Modules:
    - edge_node: Class for managing edge nodes.
    - data_processing: Functions for processing data at the edge.
"""

from .edge_node import EdgeNode
from .data_processing import process_data, aggregate_data

__all__ = [
    "EdgeNode",
    "process_data",
    "aggregate_data"
]

# Version of the edge computing module
__version__ = "1.0.0"

# Example of a simple utility function
def get_module_info():
    """Returns basic information about the edge computing module."""
    return {
        "name": "Edge Computing Module",
        "version": __version__,
        "description": "A module for managing edge computing in photonic data transmission systems."
    }
