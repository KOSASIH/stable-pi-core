# anin.test.py

import unittest
from anin import AstroNeuralInterfaceNetwork

class TestAstroNeuralInterfaceNetwork(unittest.TestCase):
    def setUp(self):
        """Set up a new AstroNeuralInterfaceNetwork instance for testing."""
        self.anin = AstroNeuralInterfaceNetwork()

    def test_connect_user_success(self):
        """Test successful user connection."""
        self.anin.connect_user("User _1", "secure-token-123")
        self.assertIn("User _1", self.anin.user_connections)

    def test_connect_user_invalid_token(self):
        """Test connection with an invalid authentication token."""
        with self.assertRaises(PermissionError) as context:
            self.anin.connect_user("User _2", "invalid-token")
        self.assertEqual(str(context.exception), "Invalid authentication token.")

    def test_disconnect_user_success(self):
        """Test successful user disconnection."""
        self.anin.connect_user("User _1", "secure-token-123")
        self.anin.disconnect_user("User _1")
        self.assertNotIn("User _1", self.anin.user_connections)

    def test_disconnect_user_not_connected(self):
        """Test disconnection of a user that is not connected."""
        with self.assertRaises(ValueError) as context:
            self.anin.disconnect_user("User _2")
        self.assertEqual(str(context.exception), "User  not connected.")

    def test_transfer_with_thought_success(self):
        """Test successful asset transfer for a connected user."""
        self.anin.connect_user("User _1", "secure-token-123")
        self.anin.transfer_with_thought("User _1", "CNC", 50)
        self.assertEqual(len(self.anin.transaction_log), 1)
        self.assertEqual(self.anin.transaction_log[0]['user_id'], "User _1")
        self.assertEqual(self.anin.transaction_log[0]['asset'], "CNC")
        self.assertEqual(self.anin.transaction_log[0]['amount'], 50)

    def test_transfer_with_thought_user_not_connected(self):
        """Test transfer when the user is not connected."""
        with self.assertRaises(ValueError) as context:
            self.anin.transfer_with_thought("User _2", "CNC", 50)
        self.assertEqual(str(context.exception), "User  not connected.")

    def test_get_transaction_log(self):
        """Test retrieval of transaction log."""
        self.anin.connect_user("User _1", "secure-token-123")
        self.anin.transfer_with_thought("User _1", "CNC", 50)
        log = self.anin.get_transaction_log()
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]['user_id'], "User _1")

    def test_check_user_status(self):
        """Test checking user connection status."""
        self.anin.connect_user("User _1", "secure-token-123")
        self.assertTrue(self.anin.check_user_status("User _1"))
        self.anin.disconnect_user("User _1")
        self.assertFalse(self.anin.check_user_status("User _1"))

if __name__ == "__main__":
    unittest.main()
