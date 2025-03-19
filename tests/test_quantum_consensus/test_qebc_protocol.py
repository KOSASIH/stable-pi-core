# tests/test_quantum_consensus/test_qebc_protocol.py

import unittest
from src.quantum_consensus.qebc_protocol import QEBCProtocol

class TestQEBCProtocol(unittest.TestCase):
    def setUp(self):
        """Set up the QEBC Protocol for testing."""
        self.node_id = 0
        self.num_nodes = 5
        self.qebc = QEBCProtocol(node_id=self.node_id, num_nodes=self.num_nodes)
        self.qebc.create_entangled_pairs()  # Create entangled pairs for the test

    def test_create_entangled_pairs(self):
        """Test that entangled pairs are created correctly."""
        self.assertEqual(len(self.qebc.entangled_pairs), self.num_nodes - 1)
        for pair in self.qebc.entangled_pairs:
            self.assertEqual(pair[0], self.node_id)  # Check that the first element is the node_id
            self.assertIn(pair[1], range(self.num_nodes))  # Check that the second element is a valid node ID

    def test_propose_value_consensus_reached(self):
        """Test proposing a value and reaching consensus."""
        proposed_value = "Test Value"
        consensus_result = self.qebc.reach_consensus(proposed_value)
        self.assertTrue(consensus_result)  # Expecting consensus to be reached

    def test_propose_value_consensus_not_reached(self):
        """Test proposing a value and not reaching consensus."""
        # Override the voting mechanism to simulate a failure in consensus
        original_vote = self.qebc._vote
        self.qebc._vote = lambda proposed_value: False  # Simulate all votes against

        proposed_value = "Test Value"
        consensus_result = self.qebc.reach_consensus(proposed_value)
        self.assertFalse(consensus_result)  # Expecting consensus not to be reached

        # Restore the original voting mechanism
        self.qebc._vote = original_vote

    def test_vote(self):
        """Test the voting mechanism."""
        proposed_value = "Test Value"
        vote_result = self.qebc._vote(proposed_value)
        self.assertIn(vote_result, [True, False])  # Vote should be either True or False

if __name__ == '__main__':
    unittest.main()
