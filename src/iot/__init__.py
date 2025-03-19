# iot/__init__.py

"""
IoT Module

This module provides functionalities for defining IoT devices, communication protocols,
and data collection from IoT devices.
"""

from .device import IoTDevice
from .communication import CommunicationProtocol
from .data_collection import collect_data

__all__ = [
    "IoTDevice",              # Class for IoT device definitions
    "CommunicationProtocol",   # Class for communication protocols
    "collect_data"            # Function to collect data from IoT devices
]

def version():
    """Return the version of the IoT module."""
    return "1.0.0"

def description():
    """Return a brief description of the IoT module."""
    return "This module implements basic functionalities for IoT devices, including communication and data collection."
