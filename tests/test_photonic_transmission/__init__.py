"""
test_photonic_transmission - Unit tests for the photonic transmission module.

This module contains unit tests for the components of the photonic transmission
system, including waveguides, modulators, photodetectors, and the transmission layer.
"""

import unittest

# Import test cases
from .test_waveguide import TestWaveguide
from .test_modulator import TestModulator
from .test_photodetector import TestPhotodetector
from .test_transmission_layer import TestTransmissionLayer

# Create a test suite
def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestWaveguide))
    suite.addTests(loader.loadTestsFromTestCase(TestModulator))
    suite.addTests(loader.loadTestsFromTestCase(TestPhotodetector))
    suite.addTests(loader.loadTestsFromTestCase(TestTransmissionLayer))
    return suite

__all__ = [
    "TestWaveguide",
    "TestModulator",
    "TestPhotodetector",
    "TestTransmissionLayer",
    "load_tests"
]
