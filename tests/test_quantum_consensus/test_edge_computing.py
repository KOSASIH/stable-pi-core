# tests/test_quantum_consensus/test_edge_computing.py

import unittest
from src.quantum_consensus.edge_computing import EdgeComputing

class TestEdgeComputing(unittest.TestCase):
    def setUp(self):
        """Set up the Edge Computing integration for testing."""
        self.node_id = 0
        self.num_nodes = 5
        self.edge_computing = EdgeComputing(node_id=self.node_id, num_nodes=self.num_nodes)

    def test_collect_data(self):
        """Test data collection functionality."""
        test_data = "Sample Data"
        self.edge_computing.collect_data(test_data)
        self.assertIn(test_data, self.edge_computing.local_data)  # Check if data is collected

    def test_process_data(self):
        """Test local data processing functionality."""
        test_data = "Sample Data"
        self.edge_computing.collect_data(test_data)
        processed_results = self.edge_computing.process_data()
        self.assertEqual(len(processed_results), 1)  # Expecting one processed result
        self.assertEqual(processed_results[0], f"Processed({test_data})")  # Check processed result

    def test_reach_consensus(self):
        """Test reaching consensus with proposed value."""
        proposed_value = "Test Value"
        self.edge_computing.collect_data(proposed_value)  # Collect data to process
        self.edge_computing.process_data()  # Process the collected data
        consensus_result = self.edge_computing.reach_consensus(proposed_value)
        self.assertTrue(consensus_result)  # Expecting consensus to be reached

    def test_vote(self):
        """Test the voting mechanism."""
        proposed_value = "Test Value"
        vote_result = self.edge_computing._vote(proposed_value)
        self.assertIn(vote_result, [True, False])  # Vote should be either True or False

if __name__ == '__main__':
    unittest.main()
