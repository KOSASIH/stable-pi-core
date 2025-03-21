# tests/test_quantum_entanglement.py

import unittest
from wdb.quantum_entanglement import QuantumEntanglement

class TestQuantumEntanglement(unittest.TestCase):
    def setUp(self):
        self.entanglement = QuantumEntanglement()

    def test_create_entangled_pair(self):
        pair = self.entanglement.create_entangled_pair()
        self.assertEqual(len(pair), 2)
        self.assertTrue(self.entanglement.verify_entanglement(pair))

    def test_measure_entangled_state(self):
        pair = self.entanglement.create_entangled_pair()
        measurement = self.entanglement.measure(pair)
        self.assertIn(measurement, ['0', '1'])

    def test_entangled_state_correlation(self):
        pair1 = self.entanglement.create_entangled_pair()
        pair2 = self.entanglement.create_entangled_pair()
        correlation = self.entanglement.check_correlation(pair1, pair2)
        self.assertTrue(correlation)

if __name__ == '__main__':
    unittest.main()
