# tests/test_quantum.py

import unittest
from quantum.quantum_solver import QuantumSolver

class TestQuantumSolver(unittest.TestCase):
    def setUp(self):
        self.solver = QuantumSolver(backend='qasm_simulator', shots=1024)

    def test_solve_optimization(self):
        problem = [100, 200, 300]
        result = self.solver.solve_optimization(problem)
        self.assertIn('solution', result)
        self.assertIn('value', result)
        self.assertIsInstance(result['solution'], str)  # Ensure solution is a string
        self.assertIsInstance(result['value'], int)      # Ensure value is an integer

if __name__ == '__main__':
    unittest.main()
