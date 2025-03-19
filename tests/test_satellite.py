# tests/test_satellite.py

import unittest
from unittest.mock import patch, MagicMock
from stsp.satellite.satellite_manager import SatelliteManager

class TestSatelliteManager(unittest.TestCase):
    @patch('stsp.satellite.satellite_manager.requests')
    def setUp(self, mock_requests):
        # Initialize the SatelliteManager with a mock API URL
        self.satellite_manager = SatelliteManager("http://localhost:5000/api/satellite")

    def test_synchronize_time(self):
        # Mock the response from the requests library
        mock_response = MagicMock()
        mock_response.json.return_value = {"synchronized_time": 1234567890}
        mock_response.status_code = 200
        self.satellite_manager.requests.get = MagicMock(return_value=mock_response)

        # Call the synchronize_time method
        synchronized_time = self.satellite_manager.synchronize_time()

        # Assertions
        self.assertEqual(synchronized_time, 1234567890)
        self.satellite_manager.requests.get.assert_called_once_with("http://localhost:5000/api/satellite/synchronize")

    def test_get_satellite_status(self):
        # Mock the response from the requests library
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "active"}
        mock_response.status_code = 200
        self.satellite_manager.requests.get = MagicMock(return_value=mock_response)

        # Call the get_satellite_status method
        status = self.satellite_manager.get_satellite_status()

        # Assertions
        self.assertEqual(status, {"status": "active"})
        self.satellite_manager.requests.get.assert_called_once_with("http://localhost:5000/api/satellite/status")

    def test_send_data_to_satellite(self):
        # Mock the response from the requests library
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "data sent"}
        mock_response.status_code = 200
        self.satellite_manager.requests.post = MagicMock(return_value=mock_response)

        # Call the send_data_to_satellite method
        response = self.satellite_manager.send_data_to_satellite({"data": "test_data"})

        # Assertions
        self.assertEqual(response, {"status": "data sent"})
        self.satellite_manager.requests.post.assert_called_once_with("http://localhost:5000/api/satellite/send", json={"data": "test_data"})

if __name__ == '__main__':
    unittest.main()
