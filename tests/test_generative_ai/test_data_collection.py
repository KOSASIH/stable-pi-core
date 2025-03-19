# tests/test_generative_ai/test_data_collection.py

import unittest
from unittest.mock import patch
from src.generative_ai.data_collection import DataCollector

class TestDataCollector(unittest.TestCase):
    def setUp(self):
        """Set up the DataCollector instance for testing."""
        self.api_url = "http://fakeapi.com/data"
        self.collector = DataCollector(api_url=self.api_url)

    @patch('src.generative_ai.data_collection.requests.get')
    def test_collect_data_success(self, mock_get):
        """Test successful data collection from the API."""
        # Mock the response from the API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "sample data"}
        
        data = self.collector.collect_data()
        
        # Assert that the collected data matches the expected output
        self.assertEqual(data, {"data": "sample data"})
        mock_get.assert_called_once_with(self.api_url)

    @patch('src.generative_ai.data_collection.requests.get')
    def test_collect_data_failure(self, mock_get):
        """Test data collection failure due to a 404 error."""
        # Mock the response to simulate a 404 error
        mock_get.return_value.status_code = 404
        
        with self.assertRaises(Exception) as context:
            self.collector.collect_data()
        
        self.assertTrue('Failed to collect data: 404' in str(context.exception))

    @patch('src.generative_ai.data_collection.requests.get')
    def test_collect_data_json_parsing_error(self, mock_get):
        """Test data collection failure due to JSON parsing error."""
        # Mock the response to simulate a successful request but with invalid JSON
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = ValueError("Invalid JSON")
        
        with self.assertRaises(Exception) as context:
            self.collector.collect_data()
        
        self.assertTrue('Error parsing JSON response' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
