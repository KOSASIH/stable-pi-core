# tests/test_tachyon_node.py

import unittest
from tcp.tachyon_node import TachyonNode
from tcp.data_packet import DataPacket

class TestTachyonNode(unittest.TestCase):
    def setUp(self):
        self.node = TachyonNode("TestNode", "localhost:8000", None)

    def test_send_data(self):
        receiver = TachyonNode("ReceiverNode", "localhost:8001", None)
        data_packet = DataPacket("TestNode", "ReceiverNode", {"message": "Hello"})
        self.node.send_data(receiver, data_packet)

        # Here you would check if the receiver received the data correctly
        # This is a placeholder for actual verification logic
        self.assertTrue(True)  # Replace with actual condition

    def test_receive_data(self):
        data_packet = DataPacket("SenderNode", "TestNode", {"message": "Hello"})
        self.node.handle_received_data(data_packet)

        # Here you would check if the node processed the data correctly
        # This is a placeholder for actual verification logic
        self.assertTrue(True)  # Replace with actual condition

if __name__ == "__main__":
    unittest.main()
