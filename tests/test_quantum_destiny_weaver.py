import unittest
from src.core.quantum_destiny_weaver import QuantumDestinyWeaver

class TestQuantumDestinyWeaver(unittest.TestCase):
    def setUp(self):
        """Setup a QuantumDestinyWeaver instance for testing."""
        self.num_qubits = 3
        self.qdw = QuantumDestinyWeaver(self.num_qubits)

    def test_create_quantum_circuit(self):
        """Test if the quantum circuit is created correctly."""
        self.qdw.create_quantum_circuit()
        self.assertEqual(self.qdw.circuit.num_qubits, self.num_qubits)
        self.assertTrue(any(self.qdw.circuit.data), "Circuit should have gates applied.")

    def test_simulate_circuit(self):
        """Test if the simulation runs without errors."""
        self.qdw.create_quantum_circuit()
        counts = self.qdw.simulate_circuit()
        self.assertIsInstance(counts, dict, "Simulation should return a dictionary of counts.")
        self.assertGreater(sum(counts.values()), 0, "Counts should not be empty.")

    def test_predict_outcomes(self):
        """Test if the predicted outcomes are probabilities."""
        self.qdw.create_quantum_circuit()
        probabilities = self.qdw.predict_outcomes()
        self.assertIsInstance(probabilities, dict, "Predicted outcomes should be a dictionary.")
        self.assertGreater(sum(probabilities.values()), 0, "Probabilities should sum to a positive value.")
        for key, value in probabilities.items():
            self.assertGreaterEqual(value, 0, "Probabilities should be non-negative.")

    def test_weave_destiny(self):
        """Test the complete process of weaving destiny."""
        probabilities = self.qdw.weave_destiny()
        self.assertIsInstance(probabilities, dict, "Weave destiny should return a dictionary of probabilities.")
        self.assertGreater(sum(probabilities.values()), 0, "Probabilities should sum to a positive value.")

if __name__ == "__main__":
    unittest.main()
