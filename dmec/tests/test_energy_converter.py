# dmec/tests/test_energy_converter.py

import unittest
from dmec.energy_converter import EnergyConverter
from dmec.config import Config

class TestEnergyConverter(unittest.TestCase):
    def setUp(self):
        """Set up a new EnergyConverter instance for each test."""
        self.converter = EnergyConverter()

    def test_initial_total_energy(self):
        """Test that the initial total energy is zero."""
        self.assertEqual(self.converter.get_total_energy(), 0)

    def test_basic_conversion(self):
        """Test the basic energy conversion."""
        interactions = 5
        total_energy = self.converter.convert(interactions)
        expected_energy = interactions * Config.DEFAULTS["ENERGY_PER_INTERACTION"]
        self.assertEqual(total_energy, expected_energy)

    def test_advanced_conversion(self):
        """Test the advanced energy conversion."""
        self.converter.conversion_strategy = "advanced"
        interactions = 5
        total_energy = self.converter.convert(interactions)
        expected_energy = interactions * Config.DEFAULTS["ENERGY_PER_INTERACTION"] * (1 + (interactions * 0.1))
        self.assertEqual(total_energy, expected_energy)

    def test_reset(self):
        """Test resetting the total energy output."""
        self.converter.convert(5)
        self.converter.reset()
        self.assertEqual(self.converter.get_total_energy(), 0)

if __name__ == '__main__':
    unittest.main()
