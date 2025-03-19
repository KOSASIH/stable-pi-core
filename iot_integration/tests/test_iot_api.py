import unittest
from unittest.mock import patch, MagicMock
from iot_api import app  # Assuming your Flask app is in iot_api.py

class TestIoTAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('iot_api.mqtt_client.publish')
    def test_receive_data(self, mock_publish):
        response = self.app.post('/iot/data', json={
            'device_id': 'device123',
            'temperature': 22.5,
            'humidity': 60
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Data received and published.', response.data)
        mock_publish.assert_called_once()

    @patch('iot_api.w3.eth.sendRawTransaction')
    def test_create_transaction(self, mock_send):
        response = self.app.post('/iot/transaction', json={
            'from_address': '0xYourAddress',
            'amount': 0.1
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Transaction created.', response.data)
        mock_send.assert_called_once()

    def test_receive_data_invalid(self):
        response = self.app.post('/iot/data', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid data format.', response.data)

if __name__ == '__main__':
    unittest.main()
