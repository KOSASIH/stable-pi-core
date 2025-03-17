import unittest
from cross_chain_bridge.bridge import CrossChainBridge

class TestCrossChainBridge(unittest.TestCase):
    def setUp(self):
        """Set up a CrossChainBridge instance for testing."""
        self.bridge = CrossChainBridge(source_chain="Ethereum", target_chain="Binance Smart Chain")

    def test_initialization(self):
        """Test the initialization of the CrossChainBridge."""
        self.assertEqual(self.bridge.source_chain, "Ethereum")
        self.assertEqual(self.bridge.target_chain, "Binance Smart Chain")
        self.assertEqual(len(self.bridge.transactions), 0)

    def test_initiate_transfer(self):
        """Test initiating a transfer."""
        transaction_id = self.bridge.initiate_transfer(amount=10.0, sender="0xSenderAddress", receiver="0xReceiverAddress")
        self.assertIn(transaction_id, [t["transaction_id"] for t in self.bridge.transactions])
        self.assertEqual(self.bridge.transactions[0]["amount"], 10.0)

    def test_confirm_transfer(self):
        """Test confirming a transfer."""
        transaction_id = self.bridge.initiate_transfer(amount=10.0, sender="0xSenderAddress", receiver="0xReceiverAddress")
        confirmed = self.bridge.confirm_transfer(transaction_id)
        self.assertTrue(confirmed)
        self.assertEqual(self.bridge.transactions[0]["status"], "confirmed")

    def test_get_transaction_status(self):
        """Test retrieving the status of a transaction."""
        transaction_id = self.bridge.initiate_transfer(amount=10.0, sender="0xSenderAddress", receiver="0xReceiverAddress")
        self.bridge.confirm_transfer(transaction_id)
        status = self.bridge.get_transaction_status(transaction_id)
        self.assertEqual(status, "confirmed")

    def test_invalid_transaction_status(self):
        """Test retrieving the status of a non-existent transaction."""
        status = self.bridge.get_transaction_status("invalid_tx_id")
        self.assertEqual(status, "Transaction not found")

if __name__ == '__main__':
    unittest.main()
