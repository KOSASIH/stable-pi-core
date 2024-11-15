import hashlib
import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

class MultiSigWallet:
    def __init__(self, required_signatures, public_keys):
        self.required_signatures = required_signatures
        self.public_keys = public_keys
        self.transactions = []

    def create_transaction(self, amount, recipient):
        transaction = {
            "amount": amount,
            "recipient": recipient,
            "status": "pending"
        }
        self.transactions.append(transaction)
        return transaction

    def sign_transaction(self, transaction, private_key):
        transaction_hash = self.hash_transaction(transaction)
        signature = private_key.sign(
            transaction_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def hash_transaction(self, transaction):
        transaction_string = json.dumps(transaction, sort_keys=True).encode()
        return hashlib.sha256(transaction_string).digest()

    def verify_signatures(self, transaction, signatures):
        transaction_hash = self.hash_transaction(transaction)
        valid_signatures = 0

        for public_key, signature in signatures.items():
            try:
                public_key.verify(
                    signature,
                    transaction_hash,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                valid_signatures += 1
            except Exception:
                continue

        return valid_signatures >= self.required_signatures

if __name__ == "__main__":
    # Example usage
    private_key1 = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key2 = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key1 = private_key1.public_key()
    public_key2 = private_key2.public_key()

    multi_sig_wallet = MultiSigWallet(required_signatures = 2, public_keys=[public_key1, public_key2])
    transaction = multi_sig_wallet.create_transaction(100, "recipient_address")
    
    signature1 = multi_sig_wallet.sign_transaction(transaction, private_key1)
    signature2 = multi_sig_wallet.sign_transaction(transaction, private_key2)

    signatures = {
        public_key1: signature1,
        public_key2: signature2
    }

    is_valid = multi_sig_wallet.verify_signatures(transaction, signatures)
    print("Transaction valid:", is_valid)
