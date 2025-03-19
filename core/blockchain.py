import hashlib
import time
import json
import logging
from typing import List, Dict, Any
from ecdsa import SigningKey, VerifyingKey, SECP256k1

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Block:
    def __init__(self, index: int, previous_hash: str, timestamp: float, transactions: List[Dict[str, Any]], nonce: int = 0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def serialize(self) -> str:
        return json.dumps(self.__dict__, sort_keys=True)

class Blockchain:
    def __init__(self, difficulty: int = 4, block_time: int = 10):
        self.chain: List[Block] = []
        self.current_transactions: List[Dict[str, Any]] = []
        self.difficulty = difficulty
        self.block_time = block_time
        self.create_block(previous_hash='1')  # Genesis block

    def create_block(self, nonce: int = 0, previous_hash: str = None) -> Block:
        block = Block(
            index=len(self.chain) + 1,
            previous_hash=previous_hash or self.chain[-1].hash,
            timestamp=time.time(),
            transactions=self.current_transactions,
            nonce=nonce
        )
        self.current_transactions = []  # Reset the current transactions
        self.chain.append(block)
        logging.info(f"Block {block.index} created with hash: {block.hash}")
        return block

    def add_transaction(self, sender: str, recipient: str, amount: float, signature: str) -> int:
        if not self.verify_signature(sender, signature):
            logging.error("Invalid transaction signature.")
            return -1  # Invalid transaction

        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'signature': signature
        }
        self.current_transactions.append(transaction)
        logging.info(f"Transaction added: {transaction}")
        return self.last_block.index + 1  # Return the index of the block that will hold this transaction

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def proof_of_work(self, previous_nonce: int) -> int:
        nonce = 0
        while not self.valid_proof(previous_nonce, nonce):
            nonce += 1
        return nonce

    def valid_proof(self, previous_nonce: int, nonce: int) -> bool:
        guess = f"{previous_nonce}{nonce}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:self.difficulty] == "0" * self.difficulty  # Adjusted difficulty

    def verify_signature(self, sender: str, signature: str) -> bool:
        try:
            verifying_key = VerifyingKey.from_string(bytes.fromhex(sender), curve=SECP256k1)
            return verifying_key.verify(bytes.fromhex(signature), self.serialize())
        except Exception as e:
            logging.error(f"Signature verification failed: {e}")
            return False

    def generate_keypair(self):
        private_key = SigningKey.generate(curve=SECP256k1)
        public_key = private_key.get_verifying_key()
        return private_key.to_string().hex(), public_key.to_string().hex()

    def __repr__(self) -> str:
        return f"Blockchain({self.chain})"

# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    
    # Generate keypair for Alice
    alice_private_key, alice_public_key = blockchain.generate_keypair()
    
    # Create a transaction
    transaction_data = {
        'sender': alice_public_key,
        'recipient': 'Bob',
        'amount': 50
    }
    transaction_string = json.dumps(transaction_data, sort_keys=True).encode()
    transaction_signature = SigningKey.from_string(bytes.fromhex(alice_private_key), curve=SECP256k1).sign(transaction_string).hex()
    
    blockchain.add_transaction(sender=alice_public_key, recipient="Bob", amount=50, signature=transaction_signature)
    previous_nonce = blockchain.last_block.nonce
    nonce = blockchain.proof_of_work(previous_nonce)
    blockchain.create_block(nonce, previous_hash=blockchain.last_block.hash)

    # Generate keypair for Bob
    bob_private_key, bob_public_key = blockchain.generate_keypair()
    
    # Create another transaction
    transaction_data = {
        'sender': bob_public_key,
        'recipient': 'Charlie',
        'amount': 25
    }
    transaction_string = json.dumps(transaction_data, sort_keys=True).encode()
    transaction_signature = SigningKey.from_string(bytes.fromhex(bob_private_key), curve=SECP256k1).sign(transaction_string).hex()
    
    blockchain.add_transaction(sender=bob_public_key, recipient="Charlie", amount=25, signature=transaction_signature)
    previous_nonce = blockchain.last_block.nonce
    nonce = blockchain.proof_of_work(previous_nonce)
    blockchain.create_block(nonce, previous_hash=blockchain.last_block.hash)

    # Print the blockchain
    for block in blockchain.chain:
        print(f"Block {block.index} Hash: {block.hash}")
        print(f"Transactions: {block.transactions}")
