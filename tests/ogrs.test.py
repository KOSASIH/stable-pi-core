# ogrs.test.py

import unittest
from ogrs import OmniGalacticResourceSymbiote

class TestOmniGalacticResourceSymbiote(unittest.TestCase):
    def setUp(self):
        """Set up a new OmniGalacticResourceSymbiote instance for testing."""
        self.ogrs = OmniGalacticResourceSymbiote()

    def test_convert_energy_success(self):
        """Test successful energy conversion."""
        self.ogrs.convert_energy("Solar Panel", 100, efficiency=0.9)
        self.assertIn("Solar Panel", self.ogrs.resources)
        self.assertEqual(self.ogrs.resources["Solar Panel"], 90)

    def test_convert_energy_negative_amount(self):
        """Test converting negative energy amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.ogrs.convert_energy("Solar Panel", -50)
        self.assertEqual(str(context.exception), "Amount of energy to convert must be non-negative.")

    def test_allocate_resources_success(self):
        """Test successful resource allocation."""
        self.ogrs.convert_energy("Solar Panel", 100, efficiency=0.9)
        self.ogrs.allocate_resources("Project Alpha", 50)
        self.assertEqual(self.ogrs.resources["Solar Panel"], 40)

    def test_allocate_resources_insufficient(self):
        """Test allocation of resources when insufficient resources are available."""
        self.ogrs.convert_energy("Solar Panel", 30, efficiency=0.9)
        with self.assertRaises(ValueError) as context:
            self.ogrs.allocate_resources("Project Alpha", 50)
        self.assertEqual(str(context.exception), "Insufficient resources available for allocation.")

    def test_allocate_resources_negative_amount(self):
        """Test allocating negative resources raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.ogrs.allocate_resources("Project Alpha", -10)
        self.assertEqual(str(context.exception), "Amount to allocate must be non-negative.")

    def test_get_resources(self):
        """Test retrieval of current resources."""
        self.ogrs.convert_energy("Solar Panel", 100, efficiency=0.9)
        resources = self.ogrs.get_resources()
        self.assertEqual(resources["Solar Panel"], 90)

    def test_get_conversion_log(self):
        """Test retrieval of conversion log."""
        self.ogrs.convert_energy("Solar Panel", 100, efficiency=0.9)
        log = self.ogrs.get_conversion_log()
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]['source'], "Solar Panel")
        self.assertEqual(log[0]['original_amount'], 100)
        self.assertEqual(log[0]['converted_amount'], 90)

if __name__ == "__main__":
    unittest.main()
