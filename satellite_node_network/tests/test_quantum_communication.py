import unittest
from satellite_node_network.quantum_communication import QuantumCommunication

class TestQuantumCommunication(unittest.TestCase):
    def setUp(self):
        """Set up a QuantumCommunication instance for testing."""
        self.quantum_comm = QuantumCommunication(node_id="Node1")

    def test_generate_quantum_key(self):
        """Test the generation of a quantum key."""
        key_length = 128
        quantum_key = self.quantum_comm.generate_quantum_key(length=key_length)
        self.assertEqual(len(quantum_key), key_length)
        self.assertTrue(all(bit in '01' for bit in quantum_key))  # Ensure the key is binary

    def test_encode_message(self):
        """Test encoding a message using a quantum key."""
        message = "10101010"
        quantum_key = "11001100"
        encoded_message = self.quantum_comm.encode_message(message, quantum_key)
        
        # Check that the encoded message is correct
        expected_encoded = ''.join(str(int(m) ^ int(k)) for m, k in zip(message, quantum_key))
        self.assertEqual(encoded_message, expected_encoded)

    def test_decode_message(self):
        """Test decoding an encoded message using a quantum key."""
        message = "10101010"
        quantum_key = "11001100"
        encoded_message = self.quantum_comm.encode_message(message, quantum_key)
        
        decoded_message = self.quantum_comm.decode_message(encoded_message, quantum_key)
        
        # Check that the decoded message matches the original message
        self.assertEqual(decoded_message, message)

    def test_secure_communication(self):
        """Test secure communication between nodes."""
        other_node = "Node2"
        message = "10101010"
        
        with self.assertLogs(level='INFO') as log:
            response = self.quantum_comm.secure_communication(other_node, message)
            self.assertIn(f"Node {self.quantum_comm.node_id} initiating secure communication with Node {other_node}.", log.output[0])
            self.assertIn(f"Encoded message sent to {other_node}: ", log.output[1])  # Check that the log contains the encoded message

if __name__ == "__main__":
    unittest.main()
