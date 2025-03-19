# tests/test_synchronization.py

import unittest
from tcp.synchronization import Synchronization

class TestSynchronization(unittest.TestCase):
    def setUp(self):
        self.sync = Synchronization()

    def test_get_current_time(self):
        current_time = self.sync.get_current_time()
        self.assertIsInstance(current_time, float)  # Check if the current time is a float

    def test_synchronize_with(self):
        remote_time = self.sync.get_current_time() + 5  # Simulate remote time
        self.sync.synchronize_with(remote_time self.assertTrue(self.sync.is_synchronized())  # Check if synchronization was successful

if __name__ == "__main__":
    unittest.main()
