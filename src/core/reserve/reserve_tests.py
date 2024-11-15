import unittest
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

    def test_adjust_reserve_increase(self):
        initial_btc = self.reserve_manager.reserve_assets["BTC"]
        self.reserve_manager.adjust_reserve("BTC", 5)
        self.assertEqual(self.reserve_manager.reserve_assets["BTC"], initial_btc + 5)

    def test_adjust_reserve_decrease(self):
        initial_eth = self.reserve_manager.reserve_assets["ETH"]
        self.reserve_manager.adjust_reserve("ETH", -10)
        self.assertEqual(self.reserve_manager.reserve_assets["ETH"], initial_eth - 10)

    def test_get_reserve_status(self):
        reserve_status, total_value = self.reserve_manager.get_reserve_status()
        self.assertEqual(reserve_status, self.reserve_manager.reserve_assets)
        self.assertIsInstance(total_value, float)

    def test_adjust_reserve_invalid_asset(self):
        initial_usd = self.reserve_manager.reserve_assets["USD"]
        self.reserve_manager.adjust_reserve("INVALID_ASSET", 100)
        self.assertEqual(self.reserve_manager.reserve_assets["USD"], initial_usd)

if __name__ == "__main__":
    unittest.main()
