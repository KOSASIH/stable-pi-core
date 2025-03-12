# iot/data_collection.py

import time
from .device import IoTDevice
from .communication import CommunicationProtocol

def collect_data(device, communication_protocol):
    """Collect data from an IoT device and send it via communication protocol.

    Args:
        device (IoTDevice): The IoT device to collect data from.
        communication_protocol (CommunicationProtocol): The communication protocol to use.
    """
    while True:
        # Simulate data collection
        data = {
            'temperature': 22.5,  # Example data
            'humidity': 60.0
        }
        device.update_data(data)
        communication_protocol.send_data(device.device_id, device.get_data())
        time.sleep(5)  # Collect data every 5 seconds
