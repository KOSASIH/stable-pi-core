# iot/device.py

class IoTDevice:
    def __init__(self, device_id, device_type, location):
        """Initialize an IoT device.

        Args:
            device_id (str): Unique identifier for the device.
            device_type (str): Type of the device (e.g., sensor, actuator).
            location (str): Location of the device.
        """
        self.device_id = device_id
        self.device_type = device_type
        self.location = location
        self.data = {}

    def update_data(self, data):
        """Update the device's data.

        Args:
            data (dict): New data to be updated.
        """
        self.data.update(data)

    def get_data(self):
        """Get the current data of the device.

        Returns:
            dict: Current data of the device.
        """
        return self.data

    def __str__(self):
        return f"{self.device_type} (ID: {self.device_id}) at {self.location}"
