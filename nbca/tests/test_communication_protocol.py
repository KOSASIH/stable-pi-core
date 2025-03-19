# nbca/tests/test_communication_protocol.py

import unittest
from nbca.communication_protocol import CommunicationProtocol

class TestCommunicationProtocol(unittest.TestCase):
    def setUp(self):
        """Set up a new CommunicationProtocol instance for each test."""
        self.protocol = CommunicationProtocol(data_format="JSON")

    def test_encode_data(self):
        """Test encoding data."""
        data = {"event_id": "NEUTRINO-1234", "energy": 0.001}
        encoded_data = self.protocol.encode_data(data)
        self.assertIsInstance(encoded_data, str)

    def test_decode_data(self):
        """Test decoding data."""
        data = {"event_id": "NEUTRINO-1234", "energy": 0.001}
        encoded_data = self.protocol.encode_data(data)
        decoded_data = self.protocol.decode_data(encoded_data)
        self.assertEqual(decoded_data, data)

    def test_send_data(self):
        """Test sending data to a destination."""
        data = {"event_id": "NEUTRINO-1234", "energy": 0.001}
        destination = "http://example.com/api"
        response = self.protocol.send_data(data, destination)
        self.assertEqual(response['status'], "success")

    def test_receive_data(self):
        """Test receiving encoded data."""
        data = {"event_id": "NEUTRINO-1234", "energy": 0.001}
        encoded_data = self.protocol.encode_data(data)
        received_data = self.protocol.receive_data(encoded_data)
        self.assertEqual(received_data, data)

if __name__ == '__main__':
    unittest.main()
