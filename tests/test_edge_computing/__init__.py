"""
test_edge_computing - Unit tests for the edge computing module.

This module contains unit tests for the components of the edge computing
system, including edge nodes and data processing functions.
"""

import unittest

# Import test cases
from .test_edge_node import TestEdgeNode
from .test_data_processing import TestDataProcessing

# Create a test suite
def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeNode))
    suite.addTests(loader.loadTestsFromTestCase(TestDataProcessing))
    return suite

__all__ = [
    "TestEdgeNode",
    "TestDataProcessing",
    "load_tests"
]
