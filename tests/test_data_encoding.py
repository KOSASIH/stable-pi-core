import unittest
import numpy as np
from holographic_data_storage.data_encoding import encode_data, decode_data

class TestDataEncoding(unittest.TestCase):
    def setUp(self):
        """Set up test data for encoding and decoding."""
        self.test_data = b'Test data for encoding.'
        self.encoded_data = encode_data(self.test_data)

    def test_encode_data(self):
        """Test the encoding of data into holographic format."""
        self.assertIsInstance(self.encoded_data, np.ndarray)
        self.assertGreater(self.encoded_data.size, 0)
        self.assertEqual(self.encoded_data.flatten().tobytes()[:len(self.test_data)], self.test_data)

    def test_decode_data(self):
        """Test the decoding of holographic data back to original format."""
        decoded_data = decode_data(self.encoded_data)
        self.assertEqual(decoded_data, self.test_data)

    def test_decode_empty_data(self):
        """Test decoding of an empty holographic array."""
        empty_array = np.zeros((0, 0, 0), dtype=np.uint8)
        decoded_data = decode_data(empty_array)
        self.assertEqual(decoded_data, b'')

    def test_decode_invalid_data(self):
        """Test decoding of invalid holographic data."""
        invalid_array = np.array([[1, 2], [3, 4]], dtype=np.uint8)  # Not a valid holographic format
        decoded_data = decode_data(invalid_array)
        self.assertIsNotNone(decoded_data)  # Should not raise an error

if __name__ == "__main__":
    unittest.main()
