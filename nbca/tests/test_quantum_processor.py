# nbca/tests/test_quantum_processor.py

import unittest
import numpy as np
from nbca.quantum_processor import QuantumProcessor

class TestQuantumProcessor(unittest.TestCase):
    def setUp(self):
        """Set up a new QuantumProcessor instance for each test."""
        self.processor = QuantumProcessor(processor_type="Photonic")

    def test_create_entangled_pair(self):
        """Test creating an entangled pair."""
        entangled_pair = self.processor.create_entangled_pair()
        self.assertEqual(entangled_pair.shape, (2,))

    def test_process_data(self):
        """Test processing data using quantum algorithms."""
        data = np.array([1, 0])  # Example qubit state |0⟩
        processed_data = self.processor.process_data(data)
        self.assertEqual(processed_data.shape, (2,))

    def test_measure_qubit(self):
        """Test measuring a qubit."""
        qubit = np.array([1, 0])  # Example qubit state |0⟩
        measurement = self.processor.measure_qubit(qubit)
        self.assertIn(measurement, [0, 1])

if __name__ == '__main__':
    unittest.main()
