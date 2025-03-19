import unittest
from unittest.mock import patch, Mock
from aqps.blockchain_integration import BlockchainIntegration

class TestBlockchainIntegration(unittest.TestCase):
    @patch('requests.post')
    def test_log_transaction_success(self, mock_post):
        # Mock the response from the blockchain API
        mock_post.return_value = Mock(status_code=200, json=lambda: {'transaction_id': 'mock_transaction_id'})
        
        blockchain = BlockchainIntegration("http://mock-blockchain-api.com")
        transaction_data = {
            "quantum_key": "example_quantum_key",
            "encrypted_data": "example_encrypted_data",
            "timestamp": "2023-10-01T12:00:00Z"
        }
        transaction_id = blockchain.log_transaction(transaction_data)
        
        self.assertEqual(transaction_id, 'mock_transaction_id')
        mock_post.assert_called_once_with("http://mock-blockchain-api.com/log_transaction", json=transaction_data)

    @patch('requests.post')
    def test_log_transaction_failure(self, mock_post):
        # Mock a failed response
        mock_post.return_value = Mock(status_code=500, text='Internal Server Error')
        
        blockchain = BlockchainIntegration("http://mock-blockchain-api.com")
        transaction_data = {
            "quantum_key": "example_quantum_key",
            "encrypted_data": "example_encrypted _data",
            "timestamp": "2023-10-01T12:00:00Z"
        }
        
        with self.assertRaises(Exception) as context:
            blockchain.log_transaction(transaction_data)
        
        self.assertIn("Failed to log transaction with status code: 500", str(context.exception))

if __name__ == '__main__':
    unittest.main()
