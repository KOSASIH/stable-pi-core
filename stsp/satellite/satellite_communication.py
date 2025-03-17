# stsp/satellite/satellite_communication.py

import logging
import requests

class SatelliteCommunication:
    """
    Implements communication protocols with satellites.
    """

    def __init__(self, satellite_api_url):
        """
        Initialize the SatelliteCommunication instance.

        :param satellite_api_url: The API URL for communicating with satellite systems.
        """
        self.satellite_api_url = satellite_api_url
        logging.info("SatelliteCommunication initialized with API URL: %s", satellite_api_url)

    def send_message(self, message):
        """
        Send a message to the satellite.

        :param message: The message to send to the satellite.
        :return: Response from the satellite system.
        """
        try:
            response = requests.post(f"{self.satellite_api_url}/send_message", json={"message": message})
            response.raise_for_status()  # Raise an error for bad responses
            logging.info("Message sent to satellite successfully: %s", message)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error("Failed to send message to satellite: %s", e)
            raise

    def receive_message(self):
        """
        Receive a message from the satellite.

        :return: The received message from the satellite.
        """
        try:
            response = requests.get(f"{self.satellite_api_url}/receive_message")
            response.raise_for_status()  # Raise an error for bad responses
            message = response.json().get("message")
            logging.info("Message received from satellite: %s", message)
            return message
        except requests.exceptions.RequestException as e:
            logging.error("Failed to receive message from satellite: %s", e)
            raise

    def get_satellite_status(self):
        """
        Get the status of the satellite system.

        :return: The status of the satellite system.
        """
        try:
            response = requests.get(f"{self.satellite_api_url}/status")
            response.raise_for_status()  # Raise an error for bad responses
            status = response.json()
            logging.info("Satellite status retrieved successfully: %s", status)
            return status
        except requests.exceptions.RequestException as e:
            logging.error("Failed to retrieve satellite status: %s", e)
            raise

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    satellite_api_url = "http://localhost:5000/api/satellite"  # Replace with actual satellite API URL
    satellite_comm = SatelliteCommunication(satellite_api_url)

    # Send a message to the satellite
    message = "Hello, Satellite!"
    response = satellite_comm.send_message(message)
    print(f"Response from Satellite: {response}")

    # Receive a message from the satellite
    received_message = satellite_comm.receive_message()
    print(f"Received Message from Satellite: {received_message}")

    # Get satellite status
    status = satellite_comm.get_satellite_status()
    print(f"Satellite Status: {status}")
