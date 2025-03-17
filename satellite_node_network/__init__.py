"""
satellite_node_network
=======================

This module provides functionalities for managing a network of satellite nodes
that support Edge Computing and Decentralized Quantum Network. It includes
classes for satellite nodes, edge computing capabilities, and quantum
communication protocols.

Public API:
-----------
- SatelliteNode: Class for managing individual satellite nodes.
- EdgeComputing: Class for processing data at the edge.
- QuantumCommunication: Class for secure quantum communication.
- NodeManager: Class for managing connections and data flow between nodes.
- load_config: Function to load configuration settings for the satellite network.
"""

from .satellite_node import SatelliteNode
from .edge_computing import EdgeComputing
from .quantum_communication import QuantumCommunication
from .node_manager import NodeManager
from .config import load_config

__all__ = [
    "SatelliteNode",
    "EdgeComputing",
    "QuantumCommunication",
    "NodeManager",
    "load_config"
]
