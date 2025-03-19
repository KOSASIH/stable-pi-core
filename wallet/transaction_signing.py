import logging
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TransactionSigning:
    def __init__(self, key_manager):
        """Initialize transaction signing with a key manager."""
        self.key_manager = key_manager

    def sign_transaction(self, transaction_data: dict, private_key) -> str:
        """Sign a transaction using the private key."""
        transaction_string = str(transaction_data).encode()
        signature = private_key.sign(
            transaction_string,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        logging.info("Transaction signed.")
        return signature.hex()

    def verify_signature(self, transaction_data: dict, signature: str, public_key) -> bool:
        """Verify the signature of a transaction."""
        transaction_string = str(transaction_data).encode()
        try:
            public_key.verify(
                bytes.fromhex(signature),
                transaction_string,
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

    def sign_multisig_transaction(self, transaction_data: dict, private_keys: list) -> list:
        """Sign a transaction with multiple private keys for multi-signature support."""
        signatures = []
        for private_key in private_keys:
            signature = self.sign_transaction(transaction_data, private_key)
            signatures.append(signature)
        logging.info("Multi-signature transaction signed.")
        return signatures

# Example usage
if __name__ == "__main__":
    from key_management import KeyManagement

    key_manager = KeyManagement()
    private_key, public_key = key_manager.generate_keypair()
    
    transaction_data = {"sender": "Alice", "recipient": "Bob", "amount": 50}
    
    transaction_signer = TransactionSigning(key_manager)
    signature = transaction_signer.sign_transaction(transaction_data, private_key)
    print(f"Transaction Signature: {signature}")

    # Verify the signature
    is_valid = transaction_signer.verify_signature(transaction_data, signature, public_key)
    print(f"Is the signature valid? {is_valid}")

    # Multi-signature example
    private_key2, public_key2 = key_manager.generate_keypair()  # Generate another key for multi-signature
    multi_signatures = transaction_signer.sign_multisig_transaction(transaction_data, [private_key, private_key2])
    print(f"Multi-signature Transaction Signatures: {multi_signatures}")
