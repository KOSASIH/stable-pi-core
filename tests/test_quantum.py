# tests/test_quantum.py

import unittest
from unittest.mock import patch, MagicMock
from stsp.quantum.quantum_key_distribution import QuantumKeyDistribution
from stsp.quantum.quantum_time_transfer import QuantumTimeTransfer

class TestQuantumKeyDistribution(unittest.TestCase):
    def setUp(self):
        self.qkd = QuantumKeyDistribution()

    def test_generate_key(self):
        key = self.qkd.generate_key(length=128)
        self.assertEqual(len(key), 128)
        self.assertTrue(all(bit in '01' for bit in key))

    def test_distribute_key(self):
        self.qkd.generate_key(length=128)
        distributed_key = self.qkd.distribute_key()
        self.assertEqual(distributed_key, self.qkd.key)

    def test_verify_key_success(self):
        self.qkd.generate_key(length=128)
        result = self.qkd.verify_key(self.qkd.key)
        self.assertTrue(result)

    def test_verify_key_failure(self):
        self.qkd.generate_key(length=128)
        result = self.qkd.verify_key("wrong_key")
        self.assertFalse(result)

class TestQuantumTimeTransfer(unittest.TestCase):
    def setUp(self):
        self.qtt = QuantumTimeTransfer()

    @patch('stsp.quantum.quantum_time_transfer.time.sleep')
    def test_transfer_time(self, mock_sleep):
        target_time = 1234567890
        transferred_time = self.qtt.transfer_time(target_time)
        self.assertEqual(transferred_time, target_time)

    def test_synchronize_time(self):
        received_time = 1234567890
        synchronized_time = self.qtt.synchronize_time(received_time)
        self.assertEqual(synchronized_time, received_time)

if __name__ == '__main__':
    unittest.main()
