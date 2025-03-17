import unittest
import numpy as np
from holographic_data_storage.holographic_storage import HolographicStorage

class TestHolographicStorage(unittest.TestCase):
    def setUp(self):
        """Set up a HolographicStorage instance for testing."""
        self.storage_capacity = 1024  # 1 KB capacity for testing
        self.holographic_storage = HolographicStorage(self.storage_capacity)

    def test_store_data_success(self):
        """Test successful storage of data."""
        data = b'Test data for holographic storage.'
        identifier = 'test_data_1'
        success = self.holographic_storage.store_data(identifier, data)
        self.assertTrue(success)
        self.assertIn(identifier, self.holographic_storage.stored_data)

    def test_store_data_exceed_capacity(self):
        """Test storage failure when exceeding capacity."""
        large_data = b'A' * (self.storage_capacity + 1)  # Data larger than capacity
        identifier = 'test_data_2'
        success = self.holographic_storage.store_data(identifier, large_data)
        self.assertFalse(success)
        self.assertNotIn(identifier, self.holographic_storage.stored_data)

    def test_retrieve_data_success(self):
        """Test successful retrieval of stored data."""
        data = b'Test data for holographic storage.'
        identifier = 'test_data_3'
        self.holographic_storage.store_data(identifier, data)
        retrieved_data = self.holographic_storage.retrieve_data(identifier)
        self.assertEqual(retrieved_data, data)

    def test_retrieve_data_not_found(self):
        """Test retrieval of data that does not exist."""
        identifier = 'non_existent_data'
        retrieved_data = self.holographic_storage.retrieve_data(identifier)
        self.assertIsNone(retrieved_data)

    def test_get_storage_usage(self):
        """Test the current storage usage."""
        self.assertEqual(self.holographic_storage.get_storage_usage(), 0)
        data = b'Test data for usage check.'
        identifier = 'test_data_4'
        self.holographic_storage.store_data(identifier, data)
        self.assertGreater(self.holographic_storage.get_storage_usage(), 0)

    def test_clear_storage(self):
        """Test clearing the storage."""
        data = b'Test data for clearing storage.'
        identifier = 'test_data_5'
        self.holographic_storage.store_data(identifier, data)
        self.holographic_storage.clear_storage()
        self.assertEqual(self.holographic_storage.get_storage_usage(), 0)
        self.assertNotIn(identifier, self.holographic_storage.stored_data)

if __name__ == "__main__":
    unittest.main()
