import unittest
from unittest.mock import patch, MagicMock
from ai_predictive_governance.data_collection import DataCollector

class TestDataCollector(unittest.TestCase):
    def setUp(self):
        """Set up a DataCollector instance for testing."""
        self.on_chain_url = "http://localhost:8545/on_chain_data"
        self.off_chain_sources = [
            "http://localhost:3000/off_chain_data_1",
            "http://localhost:3000/off_chain_data_2"
        ]
        self.data_collector = DataCollector(self.on_chain_url, self.off_chain_sources)

    @patch('ai_predictive_governance.data_collection.requests.get')
    def test_collect_on_chain_data_success(self, mock_get):
        """Test successful collection of on-chain data."""
        # Mock the response from the on-chain API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "on_chain_data"}
        mock_get.return_value = mock_response

        on_chain_data = self.data_collector.collect_on_chain_data()
        self.assertEqual(on_chain_data, {"data": "on_chain_data"})
        mock_get.assert_called_once_with(self.on_chain_url)

    @patch('ai_predictive_governance.data_collection.requests.get')
    def test_collect_on_chain_data_failure(self, mock_get):
        """Test failure to collect on-chain data."""
        # Mock the response from the on-chain API
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        on_chain_data = self.data_collector.collect_on_chain_data()
        self.assertEqual(on_chain_data, {})
        mock_get.assert_called_once_with(self.on_chain_url)

    @patch('ai_predictive_governance.data_collection.requests.get')
    def test_collect_off_chain_data_success(self, mock_get):
        """Test successful collection of off-chain data."""
        # Mock the response from the off-chain APIs
        mock_response_1 = MagicMock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = {"data": "off_chain_data_1"}
        mock_get.return_value = mock_response_1

        off_chain_data = self.data_collector.collect_off_chain_data()
        self.assertEqual(off_chain_data, [{"data": "off_chain_data_1"}])
        mock_get.assert_called_once_with(self.off_chain_sources[0])

        # Test the second off-chain source
        mock_response_2 = MagicMock()
        mock_response_2.status_code = 200
        mock_response_2.json.return_value = {"data": "off_chain_data_2"}
        mock_get.return_value = mock_response_2

        off_chain_data = self.data_collector.collect_off_chain_data()
        self.assertEqual(off_chain_data, [{"data": "off_chain_data_1"}, {"data": "off_chain_data_2"}])
        mock_get.assert_called_with(self.off_chain_sources[1])

    @patch('ai_predictive_governance.data_collection.requests.get')
    def test_collect_off_chain_data_failure(self, mock_get):
        """Test failure to collect off-chain data."""
        # Mock the response from the first off-chain API
        mock_response_1 = MagicMock()
        mock_response_1.status_code = 404
        mock_get.return_value = mock_response_1

        off_chain_data = self.data_collector.collect_off_chain_data()
        self.assertEqual(off_chain_data, [])

    @patch('ai_predictive_governance.data_collection.requests.get')
    def test_collect_data(self, mock_get):
        """Test collecting both on-chain and off-chain data."""
        # Mock the on-chain data
        mock_response_on_chain = MagicMock()
        mock_response_on_chain.status_code = 200
        mock_response_on_chain.json.return_value = {"data": "on_chain_data"}
        mock_get.return_value = mock_response_on_chain

        # Mock the off-chain data
        mock_response_off_chain = MagicMock()
        mock_response_off_chain.status_code = 200
        mock_response_off_chain.json.return_value = {"data": "off_chain_data"}
        mock_get.return_value = mock_response_off_chain

        collected_data = self.data_collector.collect_data()
        self.assertIn("on_chain", collected_data)
        self.assertIn("off_chain", collected_data)

if __name__ == "__main__":
    unittest.main()
