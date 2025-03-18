import requests
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QKDClient:
    def __init__(self, satellite_api_url):
        """
        Initialize the QKDClient with the satellite API URL.

        :param satellite_api_url: URL of the satellite QKD service
        """
        self.satellite_api_url = satellite_api_url

    def request_quantum_key(self):
        """
        Request a quantum key from the satellite.

        :return: A quantum key as a string
        :raises Exception: If the request fails or the response is invalid
        """
        try:
            logging.info("Requesting quantum key from satellite...")
            response = requests.get(f"{self.satellite_api_url}/get_key")

            # Check if the response is successful
            if response.status_code == 200:
                key_data = response.json()
                if 'quantum_key' in key_data:
                    logging.info("Quantum key received successfully.")
                    return key_data['quantum_key']
                else:
                    logging.error("Invalid response format: 'quantum_key' not found.")
                    raise Exception("Invalid response format.")
            else:
                logging.error(f"Failed to retrieve quantum key: {response.status_code} - {response.text}")
                raise Exception(f"Request failed with status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception occurred: {e}")
            raise Exception("Error occurred while requesting quantum key.")

if __name__ == "__main__":
    # Example usage
    satellite_api_url = "http://micius-satellite-api.com"  # Replace with actual satellite API URL
    qkd_client = QKDClient(satellite_api_url)

    try:
        quantum_key = qkd_client.request_quantum_key()
        print(f"Quantum Key: {quantum_key}")
    except Exception as e:
        print(f"Error: {e}")
