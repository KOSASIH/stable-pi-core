import unittest
from wallet import Wallet

class TestWallet(unittest.TestCase):
    def setUp(self):
        self.wallet1 = Wallet()
        self.wallet2 = Wallet()

    def test_initial_balance(self):
        self.assertEqual(self.wallet1.get_balance("USD"), 1000.0)
        self.assertEqual(self.wallet1.get_balance("ETH"), 5.0)
        self.assertEqual(self.wallet1.get_balance("BTC"), 0.1)

    def test_transfer_success(self):
        self.wallet1.transfer(self.wallet2, "ETH", 1.0)
        self.assertEqual(self.wallet1.get_balance("ETH"), 4.0)
        self.assertEqual(self.wallet2.get_balance("ETH"), 1.0)

    def test_transfer_insufficient_balance(self):
        with self.assertRaises(ValueError):
            self.wallet1.transfer(self.wallet2, "ETH", 10.0)

    def test_transfer_unsupported_currency(self):
        with self.assertRaises(ValueError):
            self.wallet1.transfer(self.wallet2, "LTC", 1.0)

    def test_transaction_history(self):
        self .wallet1.transfer(self.wallet2, "ETH", 1.0)
        history = self.wallet1.get_transaction_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["currency"], "ETH")
        self.assertEqual(history[0]["amount"], 1.0)
        self.assertEqual(history[0]["to"], self.wallet2.export_public_key().decode())

if __name__ == "__main__":
    unittest.main()
