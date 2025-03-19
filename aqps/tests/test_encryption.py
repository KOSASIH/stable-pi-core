import unittest
from aqps.encryption import Encryption

class TestEncryption(unittest.TestCase):
    def setUp(self):
        self.quantum_key = "example_quantum_key"
        self.encryption = Encryption(self.quantum_key)

    def test_encrypt_data(self):
        data = "Sensitive information"
        encrypted_data = self.encryption.encrypt_data(data)
        self.assertIsNotNone(encrypted_data)
        self.assertNotEqual(data, encrypted_data)

    def test_decrypt_data(self):
        data = "Sensitive information"
        encrypted_data = self.encryption.encrypt_data(data)
        decrypted_data = self.encryption.decrypt_data(encrypted_data)
        self.assertEqual(data, decrypted_data)

    def test_decrypt_invalid_data(self):
        with self.assertRaises(ValueError):
            self.encryption.decrypt_data("invalid_encrypted_data")

if __name__ == '__main__':
    unittest.main()
