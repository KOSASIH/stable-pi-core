# test_qvs.py

import unittest
from src.space.qvs.qvs import QuantumVoidSymmetron

class TestQuantumVoidSymmetron(unittest.TestCase):

    def setUp(self):
        """Set up a new instance of QuantumVoidSymmetron for testing."""
        self.qvs = QuantumVoidSymmetron()
        self.qvs.initialize_qvs()

    def test_initialization(self):
        """Test if the QVS initializes correctly."""
        self.assertIsNotNone(self.qvs.material, "Material should be initialized.")
        self.assertIsNotNone(self.qvs.antimaterial, "Antimaterial should be initialized.")
        self.assertIsNotNone(self.qvs.symmetry_state, "Symmetry state should be initialized.")

    def test_create_material(self):
        """Test the creation of material."""
        material = self.qvs.create_material()
        self.assertIn('mass', material)
        self.assertIn('charge', material)
        self.assertIn('spin', material)

    def test_create_antimaterial(self):
        """Test the creation of antimaterial."""
        antimaterial = self.qvs.create_antimaterial()
        self.assertIn('mass', antimaterial)
        self.assertIn('charge', antimaterial)
        self.assertIn('spin', antimaterial)

    def test_create_symmetry(self):
        """Test the symmetry creation between material and antimaterial."""
        symmetry = self.qvs.create_symmetry()
        self.assertIsInstance(symmetry, bool, "Symmetry state should be a boolean.")
        self.assertTrue(symmetry, "Symmetry should be valid for initialized material and antimaterial.")

    def test_generate_energy(self):
        """Test energy generation based on symmetry state."""
        self.qvs.generate_energy()
        self.assertGreater(self.qvs.energy_output, 0, "Energy output should be greater than 0 if symmetry is valid.")

    def test_distribute_energy(self):
        """Test energy distribution to a node."""
        self.qvs.generate_energy()
        self.qvs.distribute_energy("Node1")
        self.assertIn("Node1", self.qvs.node_energy_distribution, "Energy should be distributed to Node1.")
        self.assertEqual(self.qvs.node_energy_distribution["Node1"], self.qvs.energy_output, "Energy distributed should match energy output.")

    def test_reset_system(self):
        """Test the reset functionality of the QVS system."""
        self.qvs.reset_system()
        self.assertIsNone(self.qvs.material, "Material should be reset to None.")
        self.assertIsNone(self.qvs.antimaterial, "Antimaterial should be reset to None.")
        self.assertEqual(self.qvs.energy_output, 0, "Energy output should be reset to 0.")
        self.assertIsNone(self.qvs.symmetry_state, "Symmetry state should be reset to None.")
        self.assertEqual(len(self.qvs.node_energy_distribution), 0, "Node energy distribution should be cleared.")

if __name__ == "__main__":
    unittest.main()
