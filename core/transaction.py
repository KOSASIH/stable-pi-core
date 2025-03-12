import json
import hashlib
import logging
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float, signature: str):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature
        self.transaction_id = self.calculate_transaction_id()

    def calculate_transaction_id(self) -> str:
        transaction_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(transaction_string).hexdigest()

    def serialize(self) -> str:
        return json.dumps(self.__dict__, sort_keys=True)

    def is_valid(self) -> bool:
        return self.verify_signature()

    def verify_signature(self) -> bool:
        try:
            verifying_key = VerifyingKey.from_string(bytes.fromhex(self.sender), curve=SECP256k1)
            return verifying_key.verify(bytes.fromhex(self.signature), self.serialize().encode())
        except Exception as e:
            logging.error(f"Signature verification failed: {e}")
            return False

class TransactionPool:
    def __init__(self):
        self.transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> bool:
        if transaction.is_valid():
            self.transactions.append(transaction)
            logging.info(f"Transaction added to pool: {transaction.transaction_id}")
            return True
        else:
            logging.error(f"Invalid transaction: {transaction.transaction_id}")
            return False

    def get_transactions(self) -> List[Transaction]:
        return self.transactions

    def clear_transactions(self):
        self.transactions = []
        logging.info("Transaction pool cleared.")

# Example usage
if __name__ == "__main__":
    # Generate keypair for Alice
    alice_private_key, alice_public_key = SigningKey.generate(curve=SECP256k1).to_string().hex(), SigningKey.generate(curve=SECP256k1).get_verifying_key().to_string().hex()

    # Create a transaction
    transaction_data = {
        'sender': alice_public_key,
        'recipient': 'Bob',
        'amount': 50
    }
    transaction_string = json.dumps(transaction_data, sort_keys=True).encode()
    transaction_signature = SigningKey.from_string(bytes.fromhex(alice_private_key), curve=SECP256k1).sign(transaction_string).hex()

    # Create a Transaction object
    transaction = Transaction(sender=alice_public_key, recipient='Bob', amount=50, signature=transaction_signature)

    # Manage the transaction pool
    transaction_pool = TransactionPool()
    transaction_pool.add_transaction(transaction)

    # Print all transactions in the pool
    for tx in transaction_pool.get_transactions():
        print(f"Transaction ID: {tx.transaction_id}, Sender: {tx.sender}, Recipient: {tx.recipient}, Amount: {tx.amount}")
