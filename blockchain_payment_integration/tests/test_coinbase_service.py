import unittest
from unittest.mock import patch, MagicMock
from services.coinbase_service import CoinbaseService

class TestCoinbaseService(unittest.TestCase):
    def setUp(self):
        self.service = CoinbaseService()

    @patch('requests.post')
    def test_create_payment_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'data': {
                'id': 'mock_payment_id',
                'status': 'pending'
            }
        }
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        payment_data = self.service.create_payment(100.00, 'USD')
        self.assertEqual(payment_data['id'], 'mock_payment_id')
        self.assertEqual(payment_data['status'], 'pending')

    @patch('requests.post')
    def test_create_payment_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        with self.assertRaises(Exception):
            self.service.create_payment(100.00, 'USD')

    @patch('requests.get')
    def test_get_payment_status_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'data': {
                'id': 'mock_payment_id',
                'status': 'completed'
            }
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        payment_status = self.service.get_payment_status('mock_payment_id')
        self.assertEqual(payment_status['id'], 'mock_payment_id')
        self.assertEqual(payment_status['status'], 'completed')

    @patch('requests.get')
    def test_get_payment_status_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            self.service.get_payment_status('mock_payment_id')

if __name__ == '__main__':
    unittest.main()
