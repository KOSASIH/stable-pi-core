"""
cross_chain_bridge - A module for cross-chain communication.

This module provides classes and functions for implementing cross-chain
bridges that enable communication and data transfer between different
blockchain networks.

Modules:
    - bridge: Class for implementing the cross-chain bridge.
    - protocols: Definitions of protocols for cross-chain communication.
"""

from .bridge import CrossChainBridge
from .protocols import ProtocolA, ProtocolB

__all__ = [
    "CrossChainBridge",
    "ProtocolA",
    "ProtocolB"
]

# Version of the cross-chain bridge module
__version__ = "1.0.0"

# Example of a simple utility function
def get_module_info():
    """Returns basic information about the cross-chain bridge module."""
    return {
        "name": "Cross Chain Bridge Module",
        "version": __version__,
        "description": "A module for enabling cross-chain communication between blockchain networks."
    }
