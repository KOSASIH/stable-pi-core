import unittest
import numpy as np
from zpehm.src.quantum_interface import QuantumInterface

class TestQuantumInterface(unittest.TestCase):

    def setUp(self):
        """Set up a new QuantumInterface instance for testing."""
        self.qi = QuantumInterface()

    def test_initialization(self):
        """Test the initialization of the QuantumInterface."""
        self.assertIsNone(self.qi.quantum_state)

    def test_prepare_quantum_state(self):
        """Test the preparation of a valid quantum state."""
        state_vector = [1/np.sqrt(2), 1/np.sqrt(2)]  # Example: |+> state
        self.qi.prepare_quantum_state(state_vector)
        np.testing.assert_array_almost_equal(self.qi.quantum_state, state_vector)

    def test_invalid_state_vector(self):
        """Test that preparing an invalid state vector raises an error."""
        invalid_state_vector = [1, 1]  # Not normalized
        with self.assertRaises(ValueError):
            self.qi.prepare_quantum_state(invalid_state_vector)

    def test_measure_quantum_state(self):
        """Test the measurement of a prepared quantum state."""
        state_vector = [1/np.sqrt(2), 1/np.sqrt(2)]  # Example: |+> state
        self.qi.prepare_quantum_state(state_vector)
        result = self.qi.measure_quantum_state()
        self.assertIn(result, [0, 1])  # Measurement should return 0 or 1

    def test_entangle_states(self):
        """Test the entanglement of two quantum states."""
        state1 = [1, 0]  # |0>
        state2 = [0, 1]  # |1>
        entangled_state = self.qi.entangle_states(state1, state2)
        expected_entangled_state = np.kron(state1, state2)  # Kronecker product
        np.testing.assert_array_almost_equal(entangled_state, expected_entangled_state)

    def test_reset_quantum_state(self):
        """Test the reset functionality of the quantum state."""
        state_vector = [1/np.sqrt(2), 1/np.sqrt(2)]
        self.qi.prepare_quantum_state(state_vector)
        self.qi.reset_quantum_state()
        self.assertIsNone(self.qi.quantum_state)

if __name__ == "__main__":
    unittest.main()
