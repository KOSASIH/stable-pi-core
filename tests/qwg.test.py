# qwg.test.py

import unittest
from qwg import QuantumWormholeGateway

class TestQuantumWormholeGateway(unittest.TestCase):
    def setUp(self):
        """Set up a new QuantumWormholeGateway instance for testing."""
        self.qwg = QuantumWormholeGateway()

    def test_register_node_success(self):
        """Test successful node registration."""
        self.qwg.register_node("Node_A", "Earth", "secure-token-123")
        self.assertIn("Node_A", self.qwg.nodes)
        self.assertEqual(self.qwg.nodes["Node_A"]["location"], "Earth")
        self.assertEqual(self.qwg.nodes["Node_A"]["status"], "active")

    def test_register_node_invalid_token(self):
        """Test registration with an invalid authentication token."""
        with self.assertRaises(ValueError) as context:
            self.qwg.register_node("Node_B", "Mars", "invalid-token")
        self.assertEqual(str(context.exception), "Invalid authentication token.")

    def test_transfer_asset_success(self):
        """Test successful asset transfer between nodes."""
        self.qwg.register_node("Node_A", "Earth", "secure-token-123")
        self.qwg.register_node("Node_B", "Mars", "secure-token-456")
        self.qwg.transfer_asset("CNC", 100, "Node_A", "Node_B")
        self.assertEqual(len(self.qwg.transaction_log), 1)
        self.assertEqual(self.qwg.transaction_log[0]['asset'], "CNC")
        self.assertEqual(self.qwg.transaction_log[0]['amount'], 100)
        self.assertEqual(self.qwg.transaction_log[0]['from'], "Node_A")
        self.assertEqual(self.qwg.transaction_log[0]['to'], "Node_B")

    def test_transfer_asset_node_not_registered(self):
        """Test transfer when one or both nodes are not registered."""
        with self.assertRaises(ValueError) as context:
            self.qwg.transfer_asset("CNC", 100, "Node_A", "Node_B")
        self.assertEqual(str(context.exception), "Both nodes must be registered.")

    def test_transfer_asset_node_inactive(self):
        """Test transfer when one of the nodes is inactive."""
        self.qwg.register_node("Node_A", "Earth", "secure-token-123")
        self.qwg.register_node("Node_B", "Mars", "secure-token-456")
        self.qwg.nodes["Node_B"]["status"] = "inactive"  # Deactivate Node_B
        with self.assertRaises(ValueError) as context:
            self.qwg.transfer_asset("CNC", 100, "Node_A", "Node_B")
        self.assertEqual(str(context.exception), "One or both nodes are inactive.")

    def test_get_transaction_log(self):
        """Test retrieval of transaction log."""
        self.qwg.register_node("Node_A", "Earth", "secure-token-123")
        self.qwg.register_node("Node_B", "Mars", "secure-token-456")
        self.qwg.transfer_asset("CNC", 100, "Node_A", "Node_B")
        log = self.qwg.get_transaction_log()
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]['asset'], "CNC")

if __name__ == "__main__":
    unittest.main()
