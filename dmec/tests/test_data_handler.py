# dmec/tests/test_data_handler.py

import unittest
import os
from dmec.data_handler import DataHandler

class TestDataHandler(unittest.TestCase):
    def setUp(self):
        """Set up a new DataHandler instance for each test."""
        self.data_handler = DataHandler()
        self.test_json_file = self.data_handler.json_filename
        self.test_csv_file = self.data_handler.csv_filename

    def tearDown(self):
        """Clean up test files after each test."""
        if os.path.exists(self.test_json_file):
            os.remove(self.test_json_file)
        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)

    def test_save_data_json(self):
 ```python
        """Test saving data to a JSON file."""
        data = {"energy": 100, "interactions": 5}
        self.data_handler.save_data(data, format='json')
        self.assertTrue(os.path.exists(self.test_json_file))

        with open(self.test_json_file, 'r') as f:
            loaded_data = json.load(f)
            self.assertEqual(loaded_data, data)

    def test_save_data_csv(self):
        """Test saving data to a CSV file."""
        data = [["energy", "interactions"], [100, 5]]
        self.data_handler.save_data(data, format='csv')
        self.assertTrue(os.path.exists(self.test_csv_file))

        with open(self.test_csv_file, 'r') as f:
            loaded_data = [line.strip().split(',') for line in f.readlines()]
            self.assertEqual(loaded_data, data)

    def test_load_data_json(self):
        """Test loading data from a JSON file."""
        data = {"energy": 100, "interactions": 5}
        self.data_handler.save_data(data, format='json')
        loaded_data = self.data_handler.load_data(format='json')
        self.assertEqual(loaded_data, data)

    def test_load_data_csv(self):
        """Test loading data from a CSV file."""
        data = [["energy", "interactions"], [100, 5]]
        self.data_handler.save_data(data, format='csv')
        loaded_data = self.data_handler.load_data(format='csv')
        self.assertEqual(loaded_data, data)

if __name__ == '__main__':
    unittest.main()
