import logging
import os
import json
from key_management import KeyManagement
from transaction_signing import TransactionSigning
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wallet:
    def __init__(self, wallet_id: str, password: str):
        """Initialize the wallet with a unique ID and password."""
        self.wallet_id = wallet_id
        self.key_manager = KeyManagement()
        self.transaction_signer = TransactionSigning(self.key_manager)
        self.balance = 0.0  # Placeholder for wallet balance
        self.password = password
        self.encryption_key = Fernet.generate_key()  # Generate a key for encrypting sensitive data
        self.fernet = Fernet(self.encryption_key)
        self.transaction_history = []  # List to store transaction history
        logging.info(f"Wallet {self.wallet_id} initialized.")

    def generate_keys(self):
        """Generate a new key pair for the wallet."""
        private_key, public_key = self.key_manager.generate_keypair()
        logging.info(f"Keys generated for wallet {self.wallet_id}: {public_key}")
        return private_key, public_key

    def encrypt_private_key(self, private_key):
        """Encrypt the private key using the wallet's encryption key."""
        encrypted_key = self.fernet.encrypt(private_key.encode())
        return encrypted_key

    def decrypt_private_key(self, encrypted_key):
        """Decrypt the private key using the wallet's encryption key."""
        decrypted_key = self.fernet.decrypt(encrypted_key).decode()
        return decrypted_key

    def get_balance(self) -> float:
        """Get the current balance of the wallet."""
        logging.info(f"Current balance for wallet {self.wallet_id}: {self.balance}")
        return self.balance

    def update_balance(self, amount: float):
        """Update the wallet balance."""
        self.balance += amount
        logging.info(f"Updated balance for wallet {self.wallet_id}: {self.balance}")

    def record_transaction(self, transaction_data):
        """Record a transaction in the transaction history."""
        self.transaction_history.append(transaction_data)
        logging.info(f"Transaction recorded: {transaction_data}")

    def get_transaction_history(self):
        """Get the transaction history."""
        return self.transaction_history

    def save_wallet(self):
        """Save the wallet data to a file."""
        wallet_data = {
            "wallet_id": self.wallet_id,
            "balance": self.balance,
            "transaction_history": self.transaction_history,
            "encryption_key": self.encryption_key.decode()  # Store the encryption key
        }
        with open(f"{self.wallet_id}_wallet.json", "w") as f:
            json.dump(wallet_data, f)
        logging.info(f"Wallet {self.wallet_id} saved.")

    def load_wallet(self):
        """Load the wallet data from a file."""
        if os.path.exists(f"{self.wallet_id}_wallet.json"):
            with open(f"{self.wallet_id}_wallet.json", "r") as f:
                wallet_data = json.load(f)
                self.wallet_id = wallet_data["wallet_id"]
                self.balance = wallet_data["balance"]
                self.transaction_history = wallet_data["transaction_history"]
                self.encryption_key = wallet_data["encryption_key"].encode()  # Load the encryption key
                self.fernet = Fernet(self.encryption_key)
            logging.info(f"Wallet {self.wallet_id} loaded.")
        else:
            logging.error(f"Wallet file for {self.wallet_id} does not exist.")

# Example usage
if __name__ == "__main__":
    wallet = Wallet(wallet_id="Wallet1", password="securepassword")
    wallet.generate_keys()
    wallet.update_balance(100.0)
    wallet.record_transaction({"type": "credit", "amount": 100.0, "recipient": "Alice"})
    wallet.save_wallet()
    print(f"Wallet Balance: {wallet.get_balance()}")
    print(f"Transaction History: {wallet.get_transaction_history()}")
