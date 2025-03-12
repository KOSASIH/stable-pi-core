# tests/test_iot.py

import pytest
from iot.device_manager import DeviceManager  # Assuming you have a DeviceManager class

@pytest.fixture
def device_manager():
    return DeviceManager()

def test_add_device(device_manager):
    device_id = device_manager.add_device("Device1")
    assert device_id is not None
    assert device_manager.get_device(device_id) is not None

def test_remove_device(device_manager):
    device_id = device_manager.add_device("Device1")
    device_manager.remove_device(device_id)
    assert device_manager.get_device(device_id) is None
