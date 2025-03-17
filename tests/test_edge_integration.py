import unittest
import json
import socket
from holographic_data_storage.holographic_storage import HolographicStorage
from holographic_data_storage.edge_integration import EdgeIntegration

class TestEdgeIntegration(unittest.TestCase):
    def setUp(self):
        """Set up a HolographicStorage and EdgeIntegration instance for testing."""
        self.storage_capacity = 1024  # 1 KB capacity for testing
        self.holographic_storage = HolographicStorage(self.storage_capacity)
        self.edge_integration = EdgeIntegration(self.holographic_storage)

    def test_store_data_via_edge(self):
        """Test storing data through the edge integration."""
        data = b'Test data for edge integration.'
        identifier = 'test_edge_data_1'
        
        # Simulate a client request to store data
        request = {
            'action': 'store',
            'identifier': identifier,
            'data': data
        }
        self.edge_integration.handle_client(self.mock_client_socket(request))
        
        # Verify that the data was stored
        self.assertIn(identifier, self.holographic_storage.stored_data)

    def test_retrieve_data_via_edge(self):
        """Test retrieving data through the edge integration."""
        data = b'Test data for edge integration.'
        identifier = 'test_edge_data_2'
        self.holographic_storage.store_data(identifier, data)

        # Simulate a client request to retrieve data
        request = {
            'action': 'retrieve',
            'identifier': identifier
        }
        response = self.edge_integration.handle_client(self.mock_client_socket(request))
        
        # Verify that the retrieved data matches the original data
        self.assertEqual(response, data)

    def test_invalid_action(self):
        """Test handling of an invalid action request."""
        request = {
            'action': 'invalid_action',
            'identifier': 'test_edge_data_3'
        }
        response = self.edge_integration.handle_client(self.mock_client_socket(request))
        
        # Verify that the response indicates an invalid action
        self.assertIn(b'{"error": "Invalid action"}', response)

    def mock_client_socket(self, request):
        """Mock a client socket for testing."""
        class MockSocket:
            def __init__(self, request):
                self.request = json.dumps(request).encode('utf-8')

            def recv(self, buffer_size):
                return self.request

            def send(self, response):
                return response

            def close(self):
                pass

        return MockSocket(request)

if __name__ == "__main__":
    unittest.main()
