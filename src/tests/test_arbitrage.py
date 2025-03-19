import unittest
from arbitrage import ArbitrageAlgorithm

class TestArbitrage(unittest.TestCase):
    def setUp(self):
        """Set up the test case with a default arbitrage algorithm instance."""
        market_data = {
            'Asset': ['Asset1', 'Asset2'],
            'Market A Price': [100, 200],
            'Market B Price': [95, 205]
        }
        self.arbitrage_algorithm = ArbitrageAlgorithm(market_data)

    def test_identify_arbitrage_opportunities(self):
        """Test identifying arbitrage opportunities."""
        opportunities = self.arbitrage_algorithm.identify_arbitrage_opportunities()
        self.assertEqual(len(opportunities), 1, msg="Should identify one arbitrage opportunity.")
        self.assertEqual(opportunities[0]['Asset'], 'Asset1', msg="The identified opportunity should be for Asset1.")

    def test_execute_trade(self):
        """Test executing a trade based on identified arbitrage opportunities."""
        opportunities = self.arbitrage_algorithm.identify_arbitrage_opportunities()
        trade_result = self.arbitrage_algorithm.execute_trade(opportunities[0])
        self.assertTrue(trade_result['success'], msg="Trade execution should be successful.")
        self.assertEqual(trade_result['asset'], 'Asset1', msg="Trade should be executed for Asset1.")

    def test_no_arbitrage_opportunities(self):
        """Test the scenario where no arbitrage opportunities exist."""
        market_data_no_opportunity = {
            'Asset': ['Asset1', 'Asset2'],
            'Market A Price': [100, 200],
            'Market B Price': [100, 200]  # No price difference
        }
        self.arbitrage_algorithm = ArbitrageAlgorithm(market_data_no_opportunity)
        opportunities = self.arbitrage_algorithm.identify_arbitrage_opportunities()
        self.assertEqual(len(opportunities), 0, msg="Should not identify any arbitrage opportunities.")

    def test_invalid_market_data(self):
        """Test handling of invalid market data."""
        with self.assertRaises(ValueError):
            invalid_market_data = {
                'Asset': ['Asset1'],
                'Market A Price': [100]  # Missing corresponding price in Market B
            }
            self.arbitrage_algorithm = ArbitrageAlgorithm(invalid_market_data)

    def test_execute_trade_with_insufficient_funds(self):
        """Test executing a trade when there are insufficient funds."""
        opportunities = self.arbitrage_algorithm.identify_arbitrage_opportunities()
        # Mock insufficient funds scenario
        self.arbitrage_algorithm.account_balance = 0  # Set account balance to 0
        trade_result = self.arbitrage_algorithm.execute_trade(opportunities[0])
        self.assertFalse(trade_result['success'], msg="Trade execution should fail due to insufficient funds.")

if __name__ == '__main__':
    unittest.main()
