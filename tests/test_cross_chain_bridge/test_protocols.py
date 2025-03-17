import unittest
from cross_chain_bridge.protocols import ProtocolA, ProtocolB

class TestProtocolA(unittest.TestCase):
    def setUp(self):
        """Set up a ProtocolA instance for testing."""
        self.protocol_a = ProtocolA()

    def test_encode(self):
        """Test encoding data using Protocol A."""
        data = {"amount": 10, "sender": "0xSenderAddress", "receiver": "0xReceiverAddress"}
        encoded_data = self.protocol_a.encode(data)
        expected_encoded = "ProtocolA:{'amount': 10, 'sender': '0xSenderAddress', 'receiver': '0xReceiverAddress'}"
        self.assertEqual(encoded_data, expected_encoded)

    def test_decode(self):
        """Test decoding data using Protocol A."""
        encoded_data = "ProtocolA:{'amount': 10, 'sender': '0xSenderAddress', 'receiver': '0xReceiverAddress'}"
        decoded_data = self.protocol_a.decode(encoded_data)
        expected_data = {'amount': 10, 'sender': '0xSenderAddress', 'receiver': '0xReceiverAddress'}
        self.assertEqual(decoded_data, expected_data)

class TestProtocolB(unittest.TestCase):
    def setUp(self):
        """Set up a ProtocolB instance for testing."""
        self.protocol_b = ProtocolB()

    def test_encode(self):
        """Test encoding data using Protocol B."""
        data = {"amount": 10, "sender": "0xSenderAddress", "receiver": "0xReceiverAddress"}
        encoded_data = self.protocol_b.encode (data)
        expected_encoded = "ProtocolB:{'amount': 10, 'sender': '0xSenderAddress', 'receiver': '0xReceiverAddress'}"
        self.assertEqual(encoded_data, expected_encoded)

    def test_decode(self):
        """Test decoding data using Protocol B."""
        encoded_data = "ProtocolB:{'amount': 10, 'sender': '0xSenderAddress', 'receiver': '0xReceiverAddress'}"
        decoded_data = self.protocol_b.decode(encoded_data)
        expected_data = {'amount': 10, 'sender': '0xSenderAddress', 'receiver': '0xReceiverAddress'}
        self.assertEqual(decoded_data, expected_data)

if __name__ == '__main__':
    unittest.main()
