import unittest
from unittest.mock import patch, Mock
from aqps.qkd_client import QKDClient

class TestQKDClient(unittest.TestCase):
    @patch('requests.get')
    def test_request_quantum_key_success(self, mock_get):
        # Mock the response from the satellite API
        mock_get.return_value = Mock(status_code=200, json=lambda: {'quantum_key': 'mock_quantum_key'})
        
        client = QKDClient("http://mock-satellite-api.com")
        key = client.request_quantum_key()
        
        self.assertEqual(key, 'mock_quantum_key')
        mock_get.assert_called_once_with("http://mock-satellite-api.com/get_key")

    @patch('requests.get')
    def test_request_quantum_key_failure(self, mock_get):
        # Mock a failed response
        mock_get.return_value = Mock(status_code=404, text='Not Found')
        
        client = QKDClient("http://mock-satellite-api.com")
        
        with self.assertRaises(Exception) as context:
            client.request_quantum_key()
        
        self.assertIn("Request failed with status code: 404", str(context.exception))

if __name__ == '__main__':
    unittest.main()
