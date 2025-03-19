import unittest
from unittest.mock import patch, MagicMock
from synthetic_biology.data_logging import log_data_to_blockchain, BlockchainInterface

class TestBlockchainInterface(unittest.TestCase):
    def setUp(self):
        """Set up a BlockchainInterface instance for testing."""
        self.blockchain_url = "http://localhost:8545"  # Example URL
        self.api_key = "test_api_key"
        self.blockchain_interface = BlockchainInterface(self.blockchain_url, self.api_key)

    @patch('synthetic_biology.data_logging.requests.post')
    def test_log_data_success(self, mock_post):
        """Test successful logging of data to the blockchain."""
        # Mock the response from the blockchain API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response

        sensor_id = "biosensor_001"
        data = {
            "timestamp": "2025-03-17T12:00:00Z",
            "value": 42.0,
            "unit": "units"
        }

        response = self.blockchain_interface.log_data(sensor_id, data)
        self.assertEqual(response, {"status": "success"})
        mock_post.assert_called_once()

    @patch('synthetic_biology.data_logging.requests.post')
    def test_log_data_failure(self, mock_post):
        """Test failure to log data to the blockchain."""
        # Mock the response from the blockchain API
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        sensor_id = "biosensor_001"
        data = {
            "timestamp": "2025-03-17T12:00:00Z",
            "value": 42.0,
            "unit": "units"
        }

        with self.assertRaises(Exception) as context:
            self.blockchain_interface.log_data(sensor_id, data)

        self.assertTrue("Failed to log data to blockchain: Bad Request" in str(context.exception))
        mock_post.assert_called_once()

class TestDataLoggingFunction(unittest.TestCase):
    @patch('synthetic_biology.data_logging.BlockchainInterface')
    def test_log_data_to_blockchain(self, MockBlockchainInterface):
        """Test the log_data_to_blockchain function."""
        # Create a mock instance of BlockchainInterface
        mock_instance = MockBlockchainInterface.return_value
        mock_instance.log_data.return_value = {"status": "success"}

        sensor_id = "biosensor_001"
        data = {
            "timestamp": "2025-03-17T12:00:00Z",
            "value": 42.0,
            "unit": "units"
        }
        blockchain_url = "http://localhost:8545"
        api_key = "test_api_key"

        response = log_data_to_blockchain(sensor_id, data, blockchain_url, api_key)
        self.assertEqual(response, {"status": "success"})
        mock_instance.log_data.assert_called_once_with(sensor_id, data)

if __name__ == "__main__":
    unittest.main()
