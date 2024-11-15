import unittest
from encryption import EncryptionManager
from multi_sig import MultiSigWallet
from cryptography.hazmat.primitives.asymmetric import rsa

class TestEncryptionManager(unittest.TestCase):
    def setUp(self):
        self.encryption_manager = EncryptionManager()

    def test_encryption_decryption(self):
        message = "Test message"
        encrypted_message = self.encryption_manager.encrypt(message)
        decrypted_message = self.encryption_manager.decrypt(encrypted_message)
        self.assertEqual(message, decrypted_message)

    def test_export_keys(self):
        private_key = self.encryption_manager.export_private_key()
        public_key = self.encryption_manager.export_public_key()
        self.assertIsNotNone(private_key)
        self.assertIsNotNone(public_key)

class TestMultiSigWallet(unittest.TestCase):
    def setUp(self):
        self.private_key1 = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.private_key2 = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key1 = self.private_key1.public_key()
        self.public_key2 = self.private_key2.public_key()
        self.multi_sig_wallet = MultiSigWallet(required_signatures=2, public_keys=[self.public_key1, self.public_key2])

    def test_create_transaction(self):
        transaction = self.multi_sig_wallet.create_transaction(100, "recipient_address")
        self.assertEqual(transaction["amount"], 100)
        self.assertEqual(transaction["recipient"], "recipient_address")

    def test_sign_and_verify_transaction(self):
        transaction = self.multi_sig_wallet.create_transaction(100, "recipient_address")
        signature1 = self.multi_sig_wallet.sign_transaction(transaction, self.private_key1)
        signature2 = self.multi_sig_wallet.sign_transaction(transaction, self.private_key2)

        signatures = {
            self.public_key1: signature1,
            self.public_key2: signature2
        }

        is_valid = self.multi_sig_wallet.verify_signatures(transaction, signatures)
        self.assertTrue(is_valid)

if __name__ == "__main__":
    unittest.main()
