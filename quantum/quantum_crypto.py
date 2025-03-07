import logging
from ntru import NTRUEncrypt
from hashlib import sha256
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QuantumCrypto:
    def __init__(self):
        self.ntru = NTRUEncrypt()
        self.public_key, self.private_key = self.ntru.generate_keypair()
        logging.info("NTRU key pair generated.")

    def encrypt_message(self, message):
        """Encrypt a message using NTRU."""
        try:
            ciphertext = self.ntru.encrypt(self.public_key, message.encode())
            logging.info(f"Message encrypted: {message}")
            return ciphertext
        except Exception as e:
            logging.error(f"Error encrypting message: {e}")
            raise

    def decrypt_message(self, ciphertext):
        """Decrypt a message using NTRU."""
        try:
            plaintext = self.ntru.decrypt(self.private_key, ciphertext).decode()
            logging.info(f"Message decrypted: {plaintext}")
            return plaintext
        except Exception as e:
            logging.error(f"Error decrypting message: {e}")
            raise

    def hash_message(self, message):
        """Hash a message using SHA-256."""
        try:
            hashed = sha256(message.encode()).hexdigest()
            logging.info(f"Message hashed: {hashed}")
            return hashed
        except Exception as e:
            logging.error(f"Error hashing message: {e}")
            raise

# Example usage
if __name__ == "__main__":
    qc = QuantumCrypto()
    
    # Example message
    message = "Hello, Quantum World!"
    
    # Encrypt the message
    ciphertext = qc.encrypt_message(message)
    print("Encrypted:", ciphertext)
    
    # Decrypt the message
    decrypted_message = qc.decrypt_message(ciphertext)
    print("Decrypted:", decrypted_message)
    
    # Hash the message
    hashed_message = qc.hash_message(message)
    print("Hashed:", hashed_message)
