# tests/test_tachyon_protocol.py

import unittest
from tcp.tachyon_protocol import TachyonProtocol

class TestTachyonProtocol(unittest.TestCase):
    def setUp(self):
        self.protocol = TachyonProtocol()

    def test_create_message(self):
        message = self.protocol.create_message("Node1", "Node2", {"data": "Hello"})
        expected_message = '{"version": "1.0", "sender": "Node1", "receiver": "Node2", "data": {"data": "Hello"}}'
        self.assertEqual(message, expected_message)

    def test_parse_message(self):
        parsed_message = self.protocol.parse_message('{"version": "1.0", "sender": "Node1", "receiver": "Node2", "data": {"data": "Hello"}}')
        self.assertEqual(parsed_message["sender"], "Node1")

    def test_validate_message(self):
        valid_message = {"version": "1.0", "sender": "Node1", "receiver": "Node2", "data": {"data": "Hello"}}
        self.assertTrue(self.protocol.validate_message(valid_message))

if __name__ == "__main__":
    unittest.main()
