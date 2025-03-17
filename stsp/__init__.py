# stsp/__init__.py

"""
Space-Time Synchronization Protocol (STSP) Package
This package implements the Space-Time Synchronization Protocol using satellite communication,
quantum technology, edge computing, and cross-chain integration.
"""

# Importing key components of the STSP package
from .stsp_protocol import STSPProtocol
from .satellite.satellite_manager import SatelliteManager
from .quantum.quantum_key_distribution import QuantumKeyDistribution
from .quantum.quantum_time_transfer import QuantumTimeTransfer
from .edge_computing.edge_node import EdgeNode
from .cross_chain.cross_chain_bridge import CrossChainBridge

__all__ = [
    "STSPProtocol",
    "SatelliteManager",
    "QuantumKeyDistribution",
    "QuantumTimeTransfer",
    "EdgeNode",
    "CrossChainBridge"
]
