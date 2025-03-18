# tests/test_node.py

import unittest
from unittest.mock import patch
from odm.nodes.node import Node

class TestNode(unittest.TestCase):

    def setUp(self):
        """Set up test variables."""
        self.node = Node("node1", "http://localhost:5000", "test_encryption_key")

    def test_collect_data(self):
        """Test data collection functionality."""
        self.node.collect_data({"title": "Test Data", "value": 42})
        self.assertEqual(len(self.node.data), 1)

    @patch('odm.nodes.node.requests.post')
    def test_send_data(self, mock_post):
        """Test sending data to another node."""
        mock_post.return_value.status_code = 200
response = self.node.send_data("http://localhost:5001", {"title": "Test Data", "value": 42})
        self.assertEqual(response.status_code, 200)
        mock_post.assert_called_once_with("http://localhost:5001", json={"title": "Test Data", "value": 42})

    def test_receive_data(self):
        """Test receiving data from another node."""
        self.node.receive_data({"title": "Test Data", "value": 42})
        self.assertEqual(len(self.node.data), 1)
        self.assertEqual(self.node.data[0]["title"], "Test Data")

if __name__ == '__main__':
    unittest.main()
