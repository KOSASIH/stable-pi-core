import os
import json
import logging
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
from web3 import Web3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecurityProtocols:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.encryption_key = None
        self.web3 = Web3()

    def generate_key_pair(self):
        """Generate a new RSA key pair for user authentication."""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        logging.info("RSA key pair generated.")

    def save_keys(self, private_key_path, public_key_path):
        """Save the generated keys to files."""
        with open(private_key_path, 'wb') as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL
            ))
        with open(public_key_path, 'wb') as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        logging.info("Keys saved to files.")

    def load_keys(self, private_key_path, public_key_path):
        """Load keys from files."""
        with open(private_key_path, 'rb') as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
        with open(public_key_path, 'rb') as f:
            self.public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )
        logging.info("Keys loaded from files.")

    def sign_transaction(self, transaction):
        """Sign a transaction using the private key."""
        transaction_data = json.dumps(transaction).encode('utf-8')
        signature = self.private_key.sign(
            transaction_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        logging.info("Transaction signed.")
        return signature

    def verify_signature(self, transaction, signature):
        """Verify the transaction signature using the public key."""
        transaction_data = json.dumps(transaction).encode('utf-8')
        try:
            self.public_key.verify(
                signature,
                transaction_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            logging.info("Signature verified successfully.")
            return True
        except Exception as e:
            logging.error(f"Signature verification failed: {e}")
            return False

    def generate_encryption_key(self):
        """Generate a symmetric encryption key for secure communication."""
        self.encryption_key = Fernet.generate_key()
        logging.info("Encryption key generated.")

    def encrypt_message(self, message):
        """Encrypt a message using the symmetric encryption key."""
        fernet = Fernet(self.encryption_key)
        encrypted_message = fernet.encrypt(message.encode('utf-8'))
        logging.info("Message encrypted.")
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        """Decrypt a message using the symmetric encryption key."""
        fernet = Fernet(self.encryption_key)
        decrypted_message = fernet.decrypt(encrypted_message).decode('utf-8')
        logging.info("Message decrypted.")
        return decrypted_message

    def run(self):
        """Example usage of the security protocols."""
        # Generate and save keys
        self.generate_key_pair()
        self.save_keys('private_key.pem', 'public_key.pem')

        # Load keys
        self.load_keys('private_key.pem', 'public_key.pem')

        # Sign and verify a transaction
        transaction = {'to': '0xRecipientAddress', 'amount': 100}
        signature = self.sign_transaction(transaction)
        is_valid = self.verify_signature(transaction, signature)

        # Generate encryption key and encrypt/decrypt a message
        self.generate_encryption_key()
        message = "This is a secret message."
        encrypted_message = self.encrypt_message(message)
        decrypted_message = self.decrypt_message(encrypted_message)

if __name__ ```python
== "__main__":
    security_protocols = SecurityProtocols()
    security_protocols.run()
