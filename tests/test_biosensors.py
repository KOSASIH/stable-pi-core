# tests/test_biosensors.py

import unittest
from biosensors.sensor_manager import SensorManager

class TestSensorManager(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.sensor_ids = ["sensor_1", "sensor_2", "sensor_3"]
        self.manager = SensorManager(self.sensor_ids)
        self.manager.connect_sensors()

    def tearDown(self):
        """
        Clean up after each test.
        """
        self.manager.disconnect_sensors()

    def test_connect_sensors(self):
        """
        Test that sensors are connected successfully.
        """
        self.assertTrue(all(self.manager.connected_sensors.values()), "Not all sensors are connected.")

    def test_collect_data(self):
        """
        Test that data is collected from connected sensors.
        """
        collected_data = self.manager.collect_data()
        self.assertEqual(len(collected_data), len(self.sensor_ids), "Data collection did not return the expected number of sensors.")
        for sensor_id, data in collected_data.items():
            self.assertIn("temperature", data, f"Temperature data missing for {sensor_id}.")
            self.assertIn("heart_rate", data, f"Heart rate data missing for {sensor_id}.")
            self.assertIn("timestamp", data, f"Timestamp data missing for {sensor_id}.")

    def test_data_format(self):
        """
        Test that the collected data is in the correct format.
        """
        collected_data = self.manager.collect_data()
        for sensor_id, data in collected_data.items():
            self.assertIsInstance(data['temperature'], float, f"Temperature for {sensor_id} is not a float.")
            self.assertIsInstance(data['heart_rate'], int, f"Heart rate for {sensor_id} is not an int.")

if __name__ == "__main__":
    unittest.main()
