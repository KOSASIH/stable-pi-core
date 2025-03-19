# ebs/tests/test_blockchain_sync.py

import unittest
from ebs.blockchain_sync import BlockchainSync
from unittest.mock import patch, Mock

class TestBlockchainSync(unittest.TestCase):
    def setUp(self):
        """Set up a new BlockchainSync instance for each test."""
        self.blockchain_url = "http://example-blockchain.com/api"  # Replace with actual URL
        self.sync_module = BlockchainSync(blockchain_url=self.blockchain_url)

    @patch('requests.post')
    def test_sync_with_external_network_success(self, mock_post):
        """Test successful synchronization with the external blockchain network."""
        mock_post.return_value = Mock(status_code=200, json=lambda: {"message": "Success"})
        data = {"transaction_id": "12345", "data": "This is a test transaction."}
        
        response = self.sync_module.sync_with_external_network(data)
        self.assertEqual(response, {"message": "Success"})

    @patch('requests.post')
    def test_sync_with_external_network_failure(self, mock_post):
        """Test failure to synchronize with the external blockchain network."""
        mock_post.return_value = Mock(status_code=500, text="Internal Server Error")
        data = {"transaction_id": "12345", "data": "This is a test transaction."}
        
        response = self.sync_module.sync_with_external_network(data)
        self.assertIsNone(response)

    @patch('requests.get')
    def test_get_blockchain_status(self, mock_get):
        """Test retrieving the status of the external blockchain network."""
        mock_get.return_value = Mock(status_code=200, json=lambda: {"status": "active"})
        
        status = self.sync_module.get_blockchain_status()
        self.assertEqual(status, {"status": "active"})

    @patch('requests.get')
    def test_get_blockchain_status_failure(self, mock_get):
        """Test failure to retrieve the status of the external blockchain network."""
        mock_get.return_value = Mock(status_code=500, text="Internal Server Error")
        
        status = self.sync_module.get_blockchain_status()
        self.assertIsNone(status)

if __name__ == '__main__':
    unittest.main()
