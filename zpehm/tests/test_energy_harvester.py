import unittest
from zpehm.src.energy_harvester import EnergyHarvester

class TestEnergyHarvester(unittest.TestCase):

    def setUp(self):
        """Set up a new EnergyHarvester instance for testing."""
        self.harvester = EnergyHarvester(base_efficiency=0.85)
        self.harvester.harvesting_rate = 1.0  # Set harvesting rate to 1 Joule per second

    def test_initialization(self):
        """Test the initialization of the EnergyHarvester."""
        self.assertEqual(self.harvester.base_efficiency, 0.85)
        self.assertEqual(self.harvester.dynamic_efficiency, 0.85)
        self.assertEqual(self.harvester.energy_collected, 0.0)

    def test_harvest_energy(self):
        """Test the energy harvesting functionality."""
        harvested_energy = self.harvester.harvest_energy()
        self.assertGreater(harvested_energy, 0)
        self.assertEqual(self.harvester.energy_collected, harvested_energy)

    def test_energy_distribution(self):
        """Test the energy distribution functionality."""
        self.harvester.harvest_energy()  # Harvest some energy
        initial_energy = self.harvester.get_total_energy()
        distributed_energy = 0.5

        # Distribute energy and check the total
        self.harvester.distribute_energy(distributed_energy)
        self.assertEqual(self.harvester.get_total_energy(), initial_energy - distributed_energy)

        # Attempt to distribute more energy than available
        with self.assertRaises(ValueError):
            self.harvester.distribute_energy(initial_energy + 1)

    def test_dynamic_efficiency_adjustment(self):
        """Test the dynamic efficiency adjustment."""
        initial_efficiency = self.harvester.dynamic_efficiency
        self.harvester.adjust_efficiency()  # Adjust efficiency based on environmental factors
        self.assertNotEqual(initial_efficiency, self.harvester.dynamic_efficiency)

    def test_reset_energy(self):
        """Test the reset functionality."""
        self.harvester.harvest_energy()  # Harvest some energy
        self.harvester.reset_energy()
        self.assertEqual(self.harvester.energy_collected, 0.0)

if __name__ == "__main__":
    unittest.main()
