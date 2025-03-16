import unittest
from quantum_network.oracle import QuantumOracle

class TestQuantumOracle(unittest.TestCase):
    def setUp(self):
        self.oracle = QuantumOracle()

    def test_query(self):
        result = self.oracle.query("What is the state of the qubit?")
        self.assertIn(result, ["0b0", "0b1"])  # Assuming the oracle can return these states

if __name__ == '__main__':
    unittest.main()
