import unittest
from aqps.edge_node import EdgeNode
from aqps.encryption import Encryption

class TestEdgeNode(unittest.TestCase):
    def setUp(self):
        self.quantum_key = "example_quantum_key"
        self.edge_node = EdgeNode(self.quantum_key)
        self.encryption = Encryption(self.quantum_key)

    def test_process_data(self):
        data = "Sensitive information"
        encrypted_data = self.edge_node.process_data(data)
        self.assertIsNotNone(encrypted_data)
        self.assertNotEqual(data, encrypted_data)

    def test_retrieve_data(self):
        data = "Sensitive information"
        encrypted_data = self.edge_node.process_data(data)
        retrieved_data = self.edge_node.retrieve_data(encrypted_data)
        self.assertEqual(data, retrieved_data)

if __name__ == '__main__':
    unittest.main()
