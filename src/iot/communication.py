# iot/communication.py

import socket
import json

class CommunicationProtocol:
    def __init__(self, host='localhost', port=8080):
        """Initialize the communication protocol.

        Args:
            host (str): Host address for communication.
            port (int): Port number for communication.
        """
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, device_id, data):
        """Send data from an IoT device.

        Args:
            device_id (str): Unique identifier for the device.
            data (dict): Data to be sent.
        """
        message = json.dumps({'device_id': device_id, 'data': data})
        self.socket.sendto(message.encode(), (self.host, self.port))
        print(f"Data sent from {device_id}: {data}")

    def receive_data(self):
        """Receive data from IoT devices.

        Returns:
            tuple: Address and data received.
        """
        data, addr = self.socket.recvfrom(1024)
        return addr, json.loads(data.decode())
