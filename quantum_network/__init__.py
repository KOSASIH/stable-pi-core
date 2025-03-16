# quantum_network/__init__.py

"""
Quantum Network Module
This module provides functionalities for a decentralized quantum network,
including quantum nodes, communication protocols, and integration with blockchain.
"""

from .node import QuantumNode
from .communication import quantum_communication
from .oracle import QuantumOracle
from .qkd import QuantumKeyDistribution
from .utils import generate_random_key, validate_message

__all__ = [
    "QuantumNode",
    "quantum_communication",
    "QuantumOracle",
    "QuantumKeyDistribution",
    "generate_random_key",
    "validate_message"
]

# Initialize the quantum network
def initialize_network(node_id):
    """
    Initializes a quantum node in the network.
    
    Args:
        node_id (str): Unique identifier for the quantum node.
    
    Returns:
        QuantumNode: An instance of the QuantumNode class.
    """
    node = QuantumNode(node_id)
    node.create_entangled_pair()  # Create initial entangled pairs
    return node

# Example of how to use the module
if __name__ == "__main__":
    # Initialize a quantum node
    node = initialize_network("Node_1")
    print(f"Initialized {node.node_id} with entangled pairs: {node.entangled_pairs}")
