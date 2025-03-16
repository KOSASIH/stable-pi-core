import unittest
from quantum_network.node import QuantumNode

class TestQuantumNode(unittest.TestCase):
    def setUp(self):
        self.node = QuantumNode(node_id="node_1", qubit_state="0b0")

    def test_initialization(self):
        self.assertEqual(self.node.node_id, "node_1")
        self.assertEqual(self.node.qubit_state, "0b0")

    def test_update_qubit_state(self):
        self.node.update_qubit_state("0b1")
        self.assertEqual(self.node.qubit_state, "0b1")

if __name__ == '__main__':
    unittest.main()
