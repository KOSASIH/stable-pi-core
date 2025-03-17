import unittest
from satellite_node_network.node_manager import NodeManager
from satellite_node_network.satellite_node import SatelliteNode

class TestNodeManager(unittest.TestCase):
    def setUp(self):
        """Set up a NodeManager instance for testing."""
        self.node_manager = NodeManager()
        self.node1 = SatelliteNode(node_id="Node1", location="Orbit 1")
        self.node2 = SatelliteNode(node_id="Node2", location="Orbit 2")
        self.node3 = SatelliteNode(node_id="Node3", location="Orbit 3")

    def test_add_node(self):
        """Test adding a node to the manager."""
        self.node_manager.add_node(self.node1)
        self.assertIn("Node1", self.node_manager.nodes)
        self.assertEqual(self.node_manager.nodes["Node1"], self.node1)

    def test_add_duplicate_node(self):
        """Test adding a duplicate node to the manager."""
        self.node_manager.add_node(self.node1)
        self.node_manager.add_node(self.node1)  # Attempt to add the same node again
        self.assertEqual(len(self.node_manager.nodes), 1)  # Should still be 1

    def test_remove_node(self):
        """Test removing a node from the manager."""
        self.node_manager.add_node(self.node1)
        self.node_manager.remove_node("Node1")
        self.assertNotIn("Node1", self.node_manager.nodes)

    def test_remove_nonexistent_node(self):
        """Test removing a node that does not exist."""
        self.node_manager.remove_node("Node1")  # Should not raise an error
        self.assertEqual(len(self.node_manager.nodes), 0)  # Still should be 0

    def test_connect_nodes(self):
        """Test connecting two nodes."""
        self.node_manager.add_node(self.node1)
        self.node_manager.add_node(self.node2)
        self.node_manager.connect_nodes("Node1", "Node2")
        
        self.assertIn(self.node2, self.node1.connected_nodes)
        self.assertIn(self.node1, self.node2.connected_nodes)

    def test_disconnect_nodes(self):
        """Test disconnecting two nodes."""
        self.node_manager.add_node(self.node1)
        self.node_manager.add_node(self.node2)
        self.node_manager.connect_nodes("Node1", "Node2")
        self.node_manager.disconnect_nodes("Node1", "Node2")
        
        self.assertNotIn(self.node2, self.node1.connected_nodes)
        self.assertNotIn(self.node1, self.node2.connected_nodes)

    def test_send_data(self):
        """Test sending data between nodes."""
        self.node_manager.add_node(self.node1)
        self.node_manager.add_node(self.node2)
        
        with self.assertLogs(level='INFO') as log:
            data = {'temperature': 75, 'humidity': 50}
            response = self.node_manager.send_data("Node1", "Node2", data)
            self.assertIn("Node Node1 sending data to Node Node2: {'temperature': 75, 'humidity': 50}", log.output[0])
            self.assertEqual(response, "Data sent from Node1 to Node2: {'temperature': 75, 'humidity': 50}")

    def test_send_data_to_nonexistent_node(self):
        """Test sending data to a node that does not exist."""
        self.node_manager.add_node(self.node1)
        data = {'temperature': 75, 'humidity': 50}
        
        with self.assertLogs(level='ERROR') as log:
            response = self.node_manager.send_data("Node1", "Node2", data)  # Node2 does not exist
            self.assertIn("One or both nodes not found in NodeManager.", log.output[0])
            self.assertIsNone(response)

if __name__ == "__main__":
    unittest.main()
