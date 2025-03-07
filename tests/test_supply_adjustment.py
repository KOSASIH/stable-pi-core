import unittest
import pandas as pd
from algorithms.supply_adjustment import SupplyAdjustment

class TestSupplyAdjustment(unittest.TestCase):
    def setUp(self):
        self.supply_adjuster = SupplyAdjustment()
        historical_data = pd.DataFrame({
            'market_price': [100, 105, 110, 95, 90],
            'current_supply': [1000, 1100, 1200, 900, 800],
            'other_factors': [1, 2, 1, 2, 1],
            'demand': [950, 1150, 1250, 850, 750]
        })
        self.supply_adjuster.train_model(historical_data)

    def test_predict_demand(self):
        predicted_demand = self.supply_adjuster.predict_demand(105, 1000, 1)
        self.assertIsInstance(predicted_demand, float)

    def test_adjust_supply_increase(self):
        new_supply = self.supply_adjuster.adjust_supply(1000, 1100)
        self.assertGreater(new_supply, 1000)

    def test_adjust_supply_decrease(self):
        new_supply = self.supply_adjuster.adjust_supply(1000, 900)
        self.assertLess(new_supply, 1000)

if __name__ == '__main__':
    unittest.main()
