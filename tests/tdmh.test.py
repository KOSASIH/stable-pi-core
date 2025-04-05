# tdmh.test.py

import unittest
from tdmh import TransDimensionalMarketHub

class TestTransDimensionalMarketHub(unittest.TestCase):
    def setUp(self):
        """Set up a new TransDimensionalMarketHub instance for testing."""
        self.tdmh = TransDimensionalMarketHub()

    def test_list_item_success(self):
        """Test successful listing of an item."""
        self.tdmh.list_item("item_001", "Galactic Crystal", 100, "A rare crystal from the Andromeda galaxy.", 50)
        self.assertIn("item_001", self.tdmh.market_data)
        self.assertEqual(self.tdmh.market_data["item_001"]["name"], "Galactic Crystal")
        self.assertEqual(self.tdmh.market_data["item_001"]["price"], 100)
        self.assertEqual(self.tdmh.market_data["item_001"]["quantity"], 50)

    def test_trade_item_success(self):
        """Test successful trading of an item."""
        self.tdmh.list_item("item_001", "Galactic Crystal", 100, "A rare crystal from the Andromeda galaxy.", 50)
        self.tdmh.trade_item("item_001", "User _1", 5)
        self.assertEqual(self.tdmh.market_data["item_001"]["quantity"], 45)
        self.assertEqual(len(self.tdmh.transaction_log), 1)
        self.assertEqual(self.tdmh.transaction_log[0]['item_name'], "Galactic Crystal")
        self.assertEqual(self.tdmh.transaction_log[0]['buyer'], "User _1")
        self.assertEqual(self.tdmh.transaction_log[0]['quantity'], 5)

    def test_trade_item_insufficient_stock(self):
        """Test trading an item with insufficient stock."""
        self.tdmh.list_item("item_001", "Galactic Crystal", 100, "A rare crystal from the Andromeda galaxy.", 2)
        with self.assertRaises(ValueError) as context:
            self.tdmh.trade_item("item_001", "User _1", 3)
        self.assertEqual(str(context.exception), "Insufficient stock for item 'Galactic Crystal'. Available: 2, Requested: 3.")

    def test_trade_item_not_available(self):
        """Test trading an item that is not available."""
        with self.assertRaises(ValueError) as context:
            self.tdmh.trade_item("item_999", "User _1", 1)
        self.assertEqual(str(context.exception), "Item not available.")

    def test_update_price_success(self):
        """Test successful price update of an item."""
        self.tdmh.list_item("item_001", "Galactic Crystal", 100, "A rare crystal from the Andromeda galaxy.", 50)
        self.tdmh.update_price("item_001", 120)
        self.assertEqual(self.tdmh.market_data["item_001"]["price"], 120)

    def test_update_price_item_not_found(self):
        """Test updating the price of an item that is not found."""
        with self.assertRaises(ValueError) as context:
            self.tdmh.update_price("item_999", 120)
        self.assertEqual(str(context.exception), "Item not found.")

    def test_check_item_details_success(self):
        """Test successful retrieval of item details."""
        self.tdmh.list_item("item_001", "Galactic Crystal", 100, "A rare crystal from the Andromeda galaxy.", 50)
        details = self.tdmh.check_item_details("item_001")
        self.assertEqual(details["name"], "Galactic Crystal")
        self.assertEqual(details["price"], 100)

    def test_check_item_details_not_found(self):
        """Test checking details of an item that is not found."""
        with self.assertRaises(ValueError) as context:
            self.tdmh.check_item_details("item_999")
        self.assertEqual(str(context.exception), "Item not found.")

    def test_get_transaction_log(self):
        """Test retrieval of transaction log."""
        self.tdmh .list_item("item_001", "Galactic Crystal", 100, "A rare crystal from the Andromeda galaxy.", 50)
        self.tdmh.trade_item("item_001", "User  _1", 5)
        log = self.tdmh.get_transaction_log()
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]['item_name'], "Galactic Crystal")
        self.assertEqual(log[0]['buyer'], "User  _1")
        self.assertEqual(log[0]['quantity'], 5)

if __name__ == "__main__":
    unittest.main()
