import unittest
from quantum_network.communication import QuantumCommunication

class TestQuantumCommunication(unittest.TestCase):
    def setUp(self):
        self.communication = QuantumCommunication()

    def test_send_message(self):
        result = self.communication.send_message("Hello, Quantum World!")
        self.assertTrue(result)

    def test_receive_message(self):
        self.communication.send_message("Test Message")
        message = self.communication.receive_message()
        self.assertEqual(message, "Test Message")

if __name__ == '__main__':
    unittest.main()
