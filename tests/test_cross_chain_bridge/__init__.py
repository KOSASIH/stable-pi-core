"""
test_cross_chain_bridge - Unit tests for the cross-chain bridge module.

This module contains unit tests for the components of the cross-chain bridge
system, including the bridge and communication protocols.
"""

import unittest

# Import test cases
from .test_bridge import TestCrossChainBridge
from .test_protocols import TestProtocolA, TestProtocolB

# Create a test suite
def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestCrossChainBridge))
    suite.addTests(loader.loadTestsFromTestCase(TestProtocolA))
    suite.addTests(loader.loadTestsFromTestCase(TestProtocolB))
    return suite

__all__ = [
    "TestCrossChainBridge",
    "TestProtocolA",
    "TestProtocolB",
    "load_tests"
]
