import unittest
import pandas as pd
from algorithms.asset_management import AssetManagement

class TestAssetManagement(unittest.TestCase):
    def setUp(self):
        self.asset_manager = AssetManagement()
        historical_data = pd.DataFrame({
            'market_conditions': [1, 2, 1, 2, 1],
            'current_allocation': [1000, 1100, 1200, 900, 800],
            'risk_factors': [1, 2, 1, 2, 1],
            'asset_performance': [1, 0, 1, 0, 1]
        })
        self.asset_manager.train_model(historical_data)

    def test_predict_performance(self):
        predicted_performance = self.asset_manager.predict_performance(1, 1000, 1)
        self.assertIn(predicted_performance, [0, 1])

    def test_adjust_allocation_increase(self):
        current_allocations = {'Asset_A': 1000, 'Asset_B': 1100}
        new_allocations = self.asset_manager.adjust_allocation(current_allocations, 1)
        self.assertGreater(new_allocations['Asset_A'], 1000)

    def test_adjust_allocation_decrease(self):
        current_allocations = {'Asset_A': 1000, 'Asset_B': 1100}
        new_allocations = self.asset_manager.adjust_allocation(current_allocations, 0)
        self.assertLess(new_allocations['Asset_A'], 1000)

if __name__ == '__main__':
    unittest.main()
