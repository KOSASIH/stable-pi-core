import unittest
from satellite_node_network.edge_computing import EdgeComputing

class TestEdgeComputing(unittest.TestCase):
    def setUp(self):
        """Set up an EdgeComputing instance for testing."""
        self.edge_computing = EdgeComputing(node_id="Node1")

    def test_process_data(self):
        """Test processing raw data."""
        raw_data = {
            'temperature': 75,
            'humidity': 50,
            'status': 'active'
        }
        processed_data = self.edge_computing.process_data(raw_data)
        
        # Check that numeric values are normalized
        self.assertIn('temperature', processed_data)
        self.assertIn('humidity', processed_data)
        self.assertEqual(processed_data['status'], 'active')  # Non-numeric data should remain unchanged

        # Check normalization logic
        self.assertGreaterEqual(processed_data['temperature'], 0)
        self.assertLessEqual(processed_data['temperature'], 1)
        self.assertGreaterEqual(processed_data['humidity'], 0)
        self.assertLessEqual(processed_data['humidity'], 1)

    def test_normalize(self):
        """Test normalization of values."""
        value = 75
        normalized_value = self.edge_computing.normalize(value)
        self.assertEqual(normalized_value, 0.75)  # Assuming normalization is based on a range of 0 to 100

        value = 0
        normalized_value = self.edge_computing.normalize(value)
        self.assertEqual(normalized_value, 0.0)

        value = 100
        normalized_value = self.edge_computing.normalize(value)
        self.assertEqual(normalized_value, 1.0)

        value = 150  # Out of range
        normalized_value = self.edge_computing.normalize(value)
        self.assertEqual(normalized_value, 1.0)  # Clamped to 1

    def test_store_data(self):
        """Test storing processed data."""
        processed_data = {
            'temperature': 0.75,
            'humidity': 0.50
        }
        # Here we would implement the actual storage logic, but for now, we just log it
        with self.assertLogs(level='INFO') as log:
            self.edge_computing.store_data(processed_data)
            self.assertIn("Node Node1 storing processed data: {'temperature': 0.75, 'humidity': 0.50}", log.output[0])

    def test_communicate_with_node(self):
        """Test communication with another node."""
        # Simulate another node for testing
        class MockNode:
            def __init__(self, node_id):
                self.node_id = node_id

        other_node = MockNode(node_id="Node2")
        data = {'temperature': 0.75, 'humidity': 0.50}
        
        with self.assertLogs(level='INFO') as log:
            self.edge_computing.communicate_with_node(other_node, data)
            self.assertIn("Node Node1 sending data to Node Node2: {'temperature': 0.75, 'humidity': 0.50}", log.output[0])

if __name__ == "__main__":
    unittest.main()
