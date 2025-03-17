import unittest
import numpy as np
from edge_computing.edge_node import EdgeNode

class TestEdgeNode(unittest.TestCase):
    def setUp(self):
        """Set up an EdgeNode instance for testing."""
        self.edge_node = EdgeNode(node_id="Node1", processing_capacity=1e6)

    def test_initialization(self):
        """Test the initialization of the EdgeNode."""
        self.assertEqual(self.edge_node.node_id, "Node1")
        self.assertEqual(self.edge_node.processing_capacity, 1e6)
        self.assertEqual(len(self.edge_node.data_storage), 0)

    def test_receive_data(self):
        """Test receiving data."""
        data = np.array([1, 2, 3])
        self.edge_node.receive_data(data)
        self.assertEqual(len(self.edge_node.data_storage), 1)
        np.testing.assert_array_equal(self.edge_node.data_storage[0], data)

    def test_process_data(self):
        """Test processing received data."""
        self.edge_node.receive_data(np.array([1, 2, 3]))
        self.edge_node.receive_data(np.array([4, 5, 6]))
        results = self.edge_node.process_data()
        expected_results = [2.0, 5.0]  # Mean of [1, 2, 3] and [4, 5, 6]
        self.assertEqual(results, expected_results)
        self.assertEqual(len(self.edge_node.data_storage), 0)  # Data storage should be cleared

if __name__ == '__main__':
    unittest.main()
