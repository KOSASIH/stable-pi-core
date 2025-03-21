# tests/test_wormhole.py

import unittest
import asyncio
from wdb.wormhole import Wormhole

class TestWormhole(unittest.TestCase):
    def setUp(self):
        self.wormhole = Wormhole('Node1', 'Node2')

    def test_entangle_data(self):
        data = "Hello, Quantum World!"
        entangled_data = self.wormhole.entangle(data)
        self.assertIn("Entangled", entangled_data)

    def test_validate_data(self):
        self.assertTrue(self.wormhole.validate_data("Valid Data"))
        self.assertFalse(self.wormhole.validate_data(""))

    async def test_simulate_transfer(self):
        data = "Test Data"
        result = await self.wormhole.simulate_transfer(data)
        self.assertEqual(result, f"Entangled({data})")

if __name__ == '__main__':
    unittest.main()
