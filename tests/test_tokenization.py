# tests/test_tokenization.py

import unittest
from tokenization.token_generator import TokenGenerator

class TestTokenGenerator(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.token_generator = TokenGenerator()

    def test_generate_token(self):
        """
        Test that a token is generated correctly.
        """
        biological_data = {
            "id": "bio_001",
            "type": "DNA",
            "sequence": "ATCGTAGCTAGCTAGCTAGC",
            "timestamp": 1633072800
        }
        token = self.token_generator.generate_token(biological_data)
        self.assertIsNotNone(token, "Token should not be None.")
        self.assertEqual(len(token), 64, "Token length should be 64 characters (SHA-256 hash).")

    def test_encrypt_decrypt_data(self):
        """
        Test that data can be encrypted and decrypted correctly.
        """
        biological_data = {
            "id": "bio_001",
            "type": "DNA",
            "sequence": "ATCGTAGCTAGCTAGCTAGC",
            "timestamp": 1633072800
        }
        encrypted_data = self.token_generator.encrypt_data(biological_data)
        decrypted_data = self.token_generator.decrypt_data(encrypted_data)
        self.assertEqual(decrypted_data, biological_data, "Decrypted data should match the original data.")

if __name__ == "__main__":
    unittest.main()
