import unittest
from satellite_node_network.satellite_node import SatelliteNode

class TestSatelliteNode(unittest.TestCase):
    def setUp(self):
        """Set up a SatelliteNode instance for testing."""
        self.node = SatelliteNode(node_id="Node1", location="Orbit 1")
        self.connected_node = SatelliteNode(node_id="Node2", location="Orbit 2")

    def test_initialization(self):
        """Test that the node is initialized correctly."""
        self.assertEqual(self.node.node_id, "Node1")
        self.assertEqual(self.node.location, "Orbit 1")
        self.assertEqual(self.node.connected_nodes, [])
        self.assertEqual(self.node.data_storage, {})

    def test_connect_to_node(self):
        """Test connecting to another node."""
        self.node.connect_to_node(self.connected_node)
        self.assertIn(self.connected_node, self.node.connected_nodes)
        self.assertIn(self.node, self.connected_node.connected_nodes)

    def test_disconnect_from_node(self):
        """Test disconnecting from another node."""
        self.node.connect_to_node(self.connected_node)
        self.node.disconnect_from_node(self.connected_node)
        self.assertNotIn(self.connected_node, self.node.connected_nodes)
        self.assertNotIn(self.node, self.connected_node.connected_nodes)

    def test_process_data(self):
        """Test processing incoming data."""
        raw_data = {'temperature': 75, 'humidity': 50}
        processed_data = self.node.process_data(raw_data)
        self.assertIn('temperature', processed_data)
        self.assertIn('humidity', processed_data)

    def test_get_connected_nodes(self):
        """Test getting the list of connected nodes."""
        self.node.connect_to_node(self.connected_node)
        connected_nodes = self.node.get_connected_nodes()
        self.assertIn("Node2", connected_nodes)

    def test_to_json(self):
        """Test JSON serialization of the node."""
        self.node.connect_to_node(self.connected_node)
        json_data = self.node.to_json()
        self.assertIn("Node1", json_data)
        self.assertIn("Node2", json_data)

if __name__ == "__main__":
    unittest.main()
