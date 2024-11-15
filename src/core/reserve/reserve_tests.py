import unittest
from unittest.mock import patch
from reserve_manager import ReserveManager

class TestReserveManager(unittest.TestCase):
    def setUp(self):
        self.reserve_manager = ReserveManager()

    def test_initial_reserve(self):
        expected_reserve = {
            "USD": 1000000,
            "BTC": 10,
            "ETH": 100,
        }
        self.assertEqual(self.reserve_manager.reserve_assets, expected_reserve)

    @patch('reserve_manager.requests.get')
    def test_calculate_total_value(self, mock_get):
        mock_get.return_value.json.return_value = {
            "bitcoin": {"usd": 50000},
            "ethereum": {"usd": 3000},
        }
        total_value = self.reserve_manager.calculate_total_value()
        expected_value = 1000000 + (10 * 50000) + (100 * 3000)
        self.assertEqual(total_value, expected_value)

    @patch('reserve_manager.requests.get')
    def test_adjust_reserve(self, mock_get):
        mock_get.return_value.json.return_value = {
            "bitcoin": {"usd": 50000},
            "ethereum": {"usd": 3000},
        }
        self.reserve_manager.adjust_reserve("BTC", 5)
        self.assertEqual(self.reserve_manager.reserve_assets["BTC"], 15)

    @patch('reserve_manager.requests.get')
    def test_rebalance_reserves(self, mock_get):
        mock_get.return_value.json.return_value = {
            "bitcoin": {"usd": 50000},
            "ethereum": {"usd": 3000},
        }
        target_distribution = {
            "USD": 0.5,
            "BTC": 0.3,
            "ETH": 0.2,
        }
        initial_total_value = self.reserve_manager.calculate_total_value()
        self.reserve_manager.rebalance_reserves(target_distribution)
        new_total_value = self.reserve_manager.calculate_total_value()
        self.assertEqual(new_total_value, initial_total_value)  # Ensure total value remains the same

if __name__ == "__main__":
    unittest.main()
