# stsp/cross_chain/__init__.py

"""
Cross-Chain Module for Space-Time Synchronization Protocol (STSP)
This module handles cross-chain functionalities, including the implementation
of cross-chain bridges and utility functions for cross-chain operations.
"""

from .cross_chain_bridge import CrossChainBridge
from .cross_chain_utils import generate_cross_chain_message

__all__ = ["CrossChainBridge", "generate_cross_chain_message"]
