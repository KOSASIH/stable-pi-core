# ecs.test.py

import unittest
from ecs import EternalChronoStabilizer

class TestEternalChronoStabilizer(unittest.TestCase):
    def setUp(self):
        """Set up a new EternalChronoStabilizer instance for testing."""
        self.ecs = EternalChronoStabilizer()

    def test_record_transaction_success(self):
        """Test successful transaction recording."""
        self.ecs.record_transaction("tx_001", "User _1", "CNC", 100)
        self.assertIn("tx_001", self.ecs.time_stamps)
        self.assertEqual(self.ecs.time_stamps["tx_001"]['user_id'], "User _1")
        self.assertEqual(self.ecs.time_stamps["tx_001"]['asset'], "CNC")
        self.assertEqual(self.ecs.time_stamps["tx_001"]['amount'], 100)

    def test_record_transaction_duplicate_id(self):
        """Test recording a transaction with a duplicate ID."""
        self.ecs.record_transaction("tx_001", "User _1", "CNC", 100)
        with self.assertRaises(ValueError) as context:
            self.ecs.record_transaction("tx_001", "User _2", "CNC", 200)
        self.assertEqual(str(context.exception), "Transaction ID tx_001 already exists.")

    def test_verify_transaction_success(self):
        """Test successful verification of a recorded transaction."""
        self.ecs.record_transaction("tx_001", "User _1", "CNC", 100)
        result = self.ecs.verify_transaction("tx_001")
        self.assertTrue(result)

    def test_verify_transaction_not_found(self):
        """Test verification of a transaction that does not exist."""
        result = self.ecs.verify_transaction("tx_999")
        self.assertFalse(result)

    def test_get_transaction_history(self):
        """Test retrieval of transaction history."""
        self.ecs.record_transaction("tx_001", "User _1", "CNC", 100)
        self.ecs.record_transaction("tx_002", "User _2", "CNC", 200)
        history = self.ecs.get_transaction_history()
        self.assertEqual(len(history), 2)
        self.assertIn("tx_001", history)
        self.assertIn("tx_002", history)

if __name__ == "__main__":
    unittest.main()
