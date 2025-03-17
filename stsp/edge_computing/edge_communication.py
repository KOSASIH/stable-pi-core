# stsp/edge_computing/edge_communication.py

import logging
import requests

class EdgeCommunication:
    """
    Manages communication between edge nodes and satellites.
    """

    def __init__(self, satellite_api_url):
        """
        Initialize the EdgeCommunication instance.

        :param satellite_api_url: The API URL for communicating with satellite systems.
        """
        self.satellite_api_url = satellite_api_url
        logging.info("EdgeCommunication initialized with API URL: %s", satellite_api_url)

    def send_data_to_satellite(self, data):
        """
        Send processed data to the satellite.

        :param data: The data to send to the satellite.
        :return: Response from the satellite system.
        """
        try:
            response = requests.post(f"{self.satellite_api_url}/send_data", json=data)
            response.raise_for_status()  # Raise an error for bad responses
            logging.info("Data sent to satellite successfully: %s", data)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error("Failed to send data to satellite: %s", e)
            raise

    def receive_data_from_satellite(self):
        """
        Receive data from the satellite.

        :return: The received data from the satellite.
        """
        try:
            response = requests.get(f"{self.satellite_api_url}/receive_data")
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            logging.info("Data received from satellite: %s", data)
            return data
        except requests.exceptions.RequestException as e:
            logging.error("Failed to receive data from satellite: %s", e)
            raise

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    satellite_api_url = "http://localhost:5000/api/satellite"  # Replace with actual satellite API URL
    edge_comm = EdgeCommunication(satellite_api_url)

    # Simulate sending data to the satellite
    data_to_send = {"sensor_data": [1, 2, 3, 4, 5]}
    response = edge_comm.send_data_to_satellite(data_to_send)
    print(f"Response from Satellite: {response}")

    # Simulate receiving data from the satellite
    received_data = edge_comm.receive_data_from_satellite()
    print(f"Received Data from Satellite: {received_data}")
