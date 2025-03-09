import unittest
from unittest.mock import patch, MagicMock
from app import create_app  # Assuming your Flask app is created in app.py
from models.payment import PaymentStatus

class TestPaymentController(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')  # Use a testing configuration
        self.client = self.app.test_client()

    @patch('services.coinbase_service.CoinbaseService.create_payment')
    def test_create_payment(self, mock_create_payment):
        mock_create_payment.return_value = {
            'id': 'mock_payment_id',
            'status': 'pending'
        }
        response = self.client.post('/api/payments', json={
            'method': 'coinbase',
            'amount': 100.00,
            'currency': 'USD'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('mock_payment_id', response.get_data(as_text=True))

    @patch('services.coinbase_service.CoinbaseService.get_payment_status')
    def test_get_payment_status(self, mock_get_payment_status):
        mock_get_payment_status.return_value = {
            'id': 'mock_payment_id',
            'status': PaymentStatus.COMPLETED.value
        }
        response = self.client.get('/api/payments/mock_payment_id')
        self.assertEqual(response.status_code, 200)
        self.assertIn(PaymentStatus.COMPLETED.value, response.get_data(as_text=True))

    def test_create_payment_invalid(self):
        response = self.client.post('/api/payments', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required fields', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
