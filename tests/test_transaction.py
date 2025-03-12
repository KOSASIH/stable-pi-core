import unittest
from wallet.key_management import KeyManagement
from wallet.transaction_signing import TransactionSigning
from transaction import Transaction

class TestTransaction(unittest.TestCase):
    def setUp(self):
        """Set up a new transaction and key manager for testing."""
        self.key_manager = KeyManagement()
        self.private_key, self.public_key = self.key_manager.generate_keypair()
        self.transaction = Transaction(sender="Alice", recipient="Bob", amount=50)

    def test_transaction_creation(self):
        """Test creating a transaction."""
        self.assertEqual(self.transaction.sender, "Alice")
        self.assertEqual(self.transaction.recipient, "Bob")
        self.assertEqual(self.transaction.amount, 50)

    def test_sign_transaction(self):
        """Test signing a transaction."""
        transaction_signer = TransactionSigning(self.key_manager)
        signature = transaction_signer.sign_transaction(self.transaction.to_dict(), self.private_key)
        self.assertIsNotNone(signature)

    def test_verify_transaction_signature(self):
        """Test verifying a transaction's signature."""
        transaction_signer = TransactionSigning(self.key_manager)
        signature = transaction_signer.sign_transaction(self.transaction.to_dict(), self.private_key)
        is_valid = transaction_signer.verify_signature(self.transaction.to_dict(), signature, self.public_key)
        self.assertTrue(is_valid)

    def test_invalid_signature_verification(self):
        """Test verifying a transaction's signature with an invalid public key."""
        transaction_signer = TransactionSigning(self.key_manager)
        signature = transaction_signer.sign_transaction(self.transaction.to_dict(), self.private_key)

        # Create a new key pair for an invalid public key
        new_key_manager = KeyManagement()
        _, invalid_public_key = new_key_manager.generate_keypair()

        is_valid = transaction_signer.verify_signature(self.transaction.to_dict(), signature, invalid_public_key)
        self.assertFalse(is_valid)

    def test_transaction_negative_amount(self):
        """Test creating a transaction with a negative amount."""
        with self.assertRaises(ValueError):
            Transaction(sender="Alice", recipient="Bob", amount=-50)

    def test_transaction_zero_amount(self):
        """Test creating a transaction with zero amount."""
        with self.assertRaises(ValueError):
            Transaction(sender="Alice", recipient="Bob", amount=0)

    def test_transaction_to_dict(self):
        """Test converting a transaction to a dictionary."""
        transaction_dict = self.transaction.to_dict()
        self.assertEqual(transaction_dict['sender'], "Alice")
        self.assertEqual(transaction_dict['recipient'], "Bob")
        self.assertEqual(transaction_dict['amount'], 50)

if __name__ == '__main__':
    unittest.main()
