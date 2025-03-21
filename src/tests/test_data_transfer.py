# tests/test_data_transfer.py

import unittest
import asyncio
from wdb.data_transfer import DataTransferProtocol

class TestDataTransferProtocol(unittest.TestCase):
    def setUp(self):
        self.data_transfer = DataTransferProtocol()

    async def test_initiate_transfer(self):
        data = "Sample Data"
        result = await self.data_transfer.initiate_transfer('Node1', 'Node2', data)
        self.assertEqual(result, "Transfer successful.")

    def test_compress_data(self):
        data = "Hello, World!"
        compressed_data = self.data_transfer.compress_data(data)
        self.assertIsInstance(compressed_data, bytes)

    def test_encrypt_data(self):
        data = "Sensitive Data"
        encrypted_data = self.data_transfer.encrypt_data(data.encode())
        self.assertIsInstance(encrypted_data, bytes)

if __name__ == '__main__':
    unittest.main()
