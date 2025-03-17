# tests/test_quantum_consensus/test_quantum_node.py

import unittest
from src.quantum_consensus.quantum_node import QuantumNode

class TestQuantumNode(unittest.TestCase):
    def setUp(self):
        """Set up the Quantum Node for testing."""
        self.node_id = 0
        self.num_nodes = 5
        self.quantum_node = QuantumNode(node_id=self.node_id, num_nodes=self.num_nodes)
        self.quantum_node.create_entangled_pairs()  # Create entangled pairs for the test

    def test_create_entangled_pairs(self):
        """Test that entangled pairs are created correctly."""
        self.assertEqual(len(self.quantum_node.entangled_pairs), self.num_nodes - 1)
        for pair in self.quantum_node.entangled_pairs:
            self.assertEqual(pair[0], self.node_id)  # Check that the first element is the node_id
            self.assertIn(pair[1], range(self.num_nodes))  # Check that the second element is a valid node ID

    def test_propose_value(self):
        """Test proposing a value for consensus."""
        proposed_value = "Test Value"
        consensus_result = self.quantum_node.propose_value(proposed_value)
        self.assertTrue(consensus_result)  # Expecting consensus to be reached

    def test_vote(self):
        """Test the voting mechanism."""
        proposed_value = "Test Value"
        vote_result = self.quantum_node._vote(proposed_value)
        self.assertIn(vote_result, [True, False])  # Vote should be either True or False

    def test_receive_vote(self):
        """Test receiving a vote from another node."""
        proposed_value = "Test Value"
        self.quantum_node.receive_vote(True)  # Simulate receiving a 'Yes' vote
        self.quantum_node.receive_vote(False)  # Simulate receiving a 'No' vote
        # Here we would typically check internal state changes, if any

if __name__ == '__main__':
    unittest.main()
