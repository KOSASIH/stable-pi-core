# hql/tests/test_quantum_interference.py

import unittest
from hql.quantum_interference import QuantumInterference

class TestQuantumInterference(unittest.TestCase):
    def setUp(self):
        """Set up a new QuantumInterference instance for each test."""
        self.qi = QuantumInterference()
        self.test_data = "This is a test message."

    def test_basic_encoding_decoding(self):
        """Test basic encoding and decoding."""
        encoded_data = self.qi.encode(self.test_data, method='basic')
        decoded_data = self.qi.decode(encoded_data)
        self.assertEqual(decoded_data, self.test_data)

    def test_advanced_encoding_decoding(self):
        """Test advanced encoding and decoding."""
        encoded_data = self.qi.encode(self.test_data, method='advanced')
        decoded_data = self.qi.decode(encoded_data)
        self.assertNotEqual(decoded_data, self.test_data)  # Advanced encoding should change the data

    def test_invalid_encoding_method(self):
        """Test handling of an invalid encoding method."""
        with self.assertRaises(ValueError):
            self.qi.encode(self.test_data, method='invalid')

if __name__ == '__main__':
    unittest.main()
