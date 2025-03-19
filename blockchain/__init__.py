# blockchain/__init__.py

"""
Blockchain Module
This module provides functionalities for a simple blockchain implementation,
including blocks, transactions, and methods for adding new blocks.
"""

from .blockchain import Blockchain, Block

__all__ = [
    "Blockchain",
    "Block"
]

# Initialize the blockchain
def initialize_blockchain() -> Blockchain:
    """
    Initializes a new blockchain.

    Returns:
        Blockchain: An instance of the Blockchain class.
    """
    blockchain = Blockchain()
    print("Initialized a new blockchain.")
    return blockchain

# Example usage
if __name__ == "__main__":
    blockchain = initialize_blockchain()
