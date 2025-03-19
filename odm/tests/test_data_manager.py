# tests/test_data_manager.py

import unittest
from odm.data.data_manager import DataManager  # Assuming you have a DataManager class
from odm.data.data_analysis import DataAnalysis  # Assuming you have a DataAnalysis class

class TestDataManager(unittest.TestCase):

    def setUp(self):
        """Set up test variables."""
        self.data_manager = DataManager()
        self.test_data = {"title": "Test Data", "description": "This is a test."}

    def test_add_data(self):
        """Test adding data to the manager."""
        self.data_manager.add_data(self.test_data)
        self.assertIn(self.test_data, self.data_manager.data_list)

    def test_remove_data(self):
        """Test removing data from the manager."""
        self.data_manager.add_data(self.test_data)
        self.data_manager.remove_data(self.test_data)
        self.assertNotIn(self.test_data, self.data_manager.data_list)

    def test_data_analysis(self):
        """Test data analysis functionality."""
        self.data_manager.add_data(self.test_data)
        analysis_result = DataAnalysis.analyze(self.data_manager.data_list)
        self.assertIsInstance(analysis_result, dict)  # Assuming analysis returns a dict

if __name__ == '__main__':
    unittest.main()
