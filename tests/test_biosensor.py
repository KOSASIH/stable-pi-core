import unittest
from synthetic_biology.biosensor import Biosensor, BiosensorManager
from datetime import datetime
import random

class TestBiosensor(unittest.TestCase):
    def setUp(self):
        """Set up a Biosensor instance for testing."""
        self.sensor_id = "biosensor_001"
        self.sensor_type = "DNA"
        self.biosensor = Biosensor(sensor_id=self.sensor_id, sensor_type=self.sensor_type)

    def test_collect_data(self):
        """Test data collection from the biosensor."""
        data = self.biosensor.collect_data()
        self.assertIn("timestamp", data)
        self.assertIn("value", data)
        self.assertIn("unit", data)
        self.assertIsInstance(data["value"], (int, float))

    def test_deactivate(self):
        """Test deactivating the biosensor."""
        self.biosensor.deactivate()
        self.assertFalse(self.biosensor.is_active)

    def test_activate(self):
        """Test activating the biosensor."""
        self.biosensor.deactivate()  # Ensure it's deactivated first
        self.biosensor.activate()
        self.assertTrue(self.biosensor.is_active)

    def test_get_status(self):
        """Test getting the status of the biosensor."""
        self.assertEqual(self.biosensor.get_status(), "Active")
        self.biosensor.deactivate()
        self.assertEqual(self.biosensor.get_status(), "Inactive")

    def test_to_json(self):
        """Test converting biosensor data to JSON format."""
        data_json = self.biosensor.to_json()
        self.assertIn("sensor_id", data_json)
        self.assertIn("sensor_type", data_json)
        self.assertIn("data", data_json)
        self.assertIn("is_active", data_json)

class TestBiosensorManager(unittest.TestCase):
    def setUp(self):
        """Set up a BiosensorManager instance for testing."""
        self.manager = BiosensorManager()
        self.biosensor1 = Biosensor("biosensor_001", "DNA")
        self.biosensor2 = Biosensor("biosensor_002", "Glucose")
        self.manager.add_biosensor(self.biosensor1)
        self.manager.add_biosensor(self.biosensor2)

    def test_add_biosensor(self):
        """Test adding a biosensor to the manager."""
        self.assertIn("biosensor_001", self.manager.biosensors)
        self.assertIn("biosensor_002", self.manager.biosensors)

    def test_remove_biosensor(self):
        """Test removing a biosensor from the manager."""
        self.manager.remove_biosensor("biosensor_001")
        self.assertNotIn("biosensor_001", self.manager.biosensors)

    def test_collect_data_from_all(self):
        """Test collecting data from all managed biosensors."""
        collected_data = self.manager.collect_data_from_all()
        self.assertIn("biosensor_001", collected_data)
        self.assertIn("biosensor_002", collected_data)

    def test_get_biosensor_status(self):
        """Test getting the status of all managed biosensors."""
        status = self.manager.get_biosensor_status()
        self.assertEqual(status["biosensor_001"], "Active")
        self.assertEqual(status["biosensor_002"], "Active")

if __name__ == "__main__":
    unittest.main()
