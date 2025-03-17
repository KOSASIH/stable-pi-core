"""
photonic_transmission - A module for photonic data transmission.

This module provides classes and functions for implementing
photonic transmission systems, including waveguides, modulators,
photodetectors, and the main transmission layer.

Modules:
    - waveguide: Implementation of waveguide for light transmission.
    - modulator: Implementation of modulator for encoding data.
    - photodetector: Implementation of photodetector for signal reception.
    - transmission_layer: Main class for the photonic data transmission layer.
"""

from .waveguide import Waveguide
from .modulator import Modulator
from .photodetector import Photodetector
from .transmission_layer import TransmissionLayer

__all__ = [
    "Waveguide",
    "Modulator",
    "Photodetector",
    "TransmissionLayer"
]

# Version of the photonic transmission module
__version__ = "1.0.0"

# Example of a simple utility function
def get_module_info():
    """Returns basic information about the photonic transmission module."""
    return {
        "name": "Photonic Transmission Module",
        "version": __version__,
        "description": "A module for implementing photonic data transmission systems."
    }
