import hashlib
import json
import logging
from typing import List, Dict, Any
from transaction import Transaction

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Block:
    def __init__(self, index: int, previous_hash: str, timestamp: float, transactions: List[Transaction], nonce: int = 0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps(self.serialize(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def serialize(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'transactions': [tx.serialize() for tx in self.transactions],
            'nonce': self.nonce,
            'hash': self.hash
        }

    def is_valid(self) -> bool:
        # Check if the block's hash is valid
        if self.hash != self.calculate_hash():
            logging.error(f"Invalid block hash for block {self.index}.")
            return False
        
        # Validate each transaction in the block
        for transaction in self.transactions:
            if not transaction.is_valid():
                logging.error(f"Invalid transaction in block {self.index}: {transaction.transaction_id}.")
                return False
        
        return True

    def __repr__(self) -> str:
        return f"Block(index={self.index}, hash={self.hash}, transactions={self.transactions})"

# Example usage
if __name__ == "__main__":
    # Create a sample transaction
    transaction = Transaction(sender="AlicePublicKey", recipient="BobPublicKey", amount=50, signature="SampleSignature")

    # Create a block
    block = Block(index=1, previous_hash='0', timestamp=1633072800, transactions=[transaction], nonce=0)

    # Validate the block
    if block.is_valid():
        logging.info(f"Block {block.index} is valid with hash: {block.hash}")
    else:
        logging.error(f"Block {block.index} is invalid.")
