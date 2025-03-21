# tests/test_node_network.py

import unittest
import asyncio
from wdb.node_network import NodeNetwork

class TestNodeNetwork(unittest.TestCase):
    def setUp(self):
        self.network = NodeNetwork()

    def test_add_node(self):
        self.network.add_node('Node1', 'LocationA')
        self.assertIn('Node1', self.network.nodes)

    def test_remove_node(self):
        self.network.add_node('Node1', 'LocationA')
        self.network.remove_node('Node1')
        self.assertNotIn('Node1', self.network.nodes)

    async def test_monitor_nodes(self):
        self.network.add_node('Node1', 'LocationA')
        await self.network.monitor_nodes()  # This will run indefinitely; consider modifying for tests

if __name__ == '__main__':
    unittest.main()
