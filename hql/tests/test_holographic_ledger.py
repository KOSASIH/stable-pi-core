# hql/tests/test_holographic_ledger.py

import unittest
from hql.holographic_ledger import HolographicQuantumLedger
from hql.config import Config
import os

class TestHolographicQuantumLedger(unittest.TestCase):
    def setUp(self):
        """Set up a new HolographicQuantumLedger instance for each test."""
        self.ledger = HolographicQuantumLedger()
        self.test_key = "test_key"
        self.test_value = "This is a test value."
        self.test_filename = "test_hql_data.json"

    def tearDown(self):
        """Clean up test files after each test."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_store_and_retrieve_data(self):
        """Test storing and retrieving data."""
        self.ledger.store_data(self.test_key, self.test_value)
        retrieved_value = self.ledger.retrieve_data(self.test_key)
        self.assertEqual(retrieved_value, self.test_value)

    def test_export_import_data(self):
        """Test exporting and importing data."""
        self.ledger.store_data(self.test_key, self.test_value)
        self.ledger.export_data(self.test_filename)
        
        new_ledger = HolographicQuantumLedger()
        new_ledger.import_data(self.test_filename)
        retrieved_value = new_ledger.retrieve_data(self.test_key)
        self.assertEqual(retrieved_value, self.test_value)

    def test_cleanup_old_entries(self):
        """Test cleanup of old entries based on retention period."""
        # Set retention period to 0 for testing
        Config.DEFAULTS["DATA_RETENTION_PERIOD"] = 0
        self.ledger.store_data(self.test_key, self.test_value)
        self.ledger.cleanup_old_entries()
        retrieved_value = self.ledger.retrieve_data(self.test_key)
        self.assertIsNone(retrieved_value)

if __name__ == '__main__':
    unittest.main()
