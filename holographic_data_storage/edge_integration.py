import socket
import json
import logging
from holographic_storage import HolographicStorage

class EdgeIntegration:
    """
    A class to manage the integration of edge computing with holographic storage.

    Attributes:
        storage (HolographicStorage): An instance of the HolographicStorage class.
        host (str): The host address for the edge device.
        port (int): The port number for the edge device.
    """

    def __init__(self, storage: HolographicStorage, host: str = 'localhost', port: int = 5000):
        """
        Initializes the EdgeIntegration instance.

        Args:
            storage (HolographicStorage): An instance of the HolographicStorage class.
            host (str): The host address for the edge device.
            port (int): The port number for the edge device.
        """
        self.storage = storage
        self.host = host
        self.port = port
        self.server_socket = None
        logging.basicConfig(level=logging.INFO)

    def start_server(self):
        """
        Starts the edge computing server to listen for incoming data.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        logging.info(f"Edge computing server started at {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server_socket.accept()
            logging.info(f"Connection established with {addr}")
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        """
        Handles communication with a connected client.

        Args:
            client_socket (socket.socket): The socket object for the connected client.
        """
        try:
            data = client_socket.recv(1024)
            if not data:
                return

            request = json.loads(data.decode('utf-8'))
            action = request.get('action')

            if action == 'store':
                identifier = request.get('identifier')
                data_to_store = request.get('data')
                self.store_data(identifier, data_to_store)
            elif action == 'retrieve':
                identifier = request.get('identifier')
                self.retrieve_data(identifier, client_socket)
            else:
                logging.error("Invalid action requested.")
                client_socket.send(b'{"error": "Invalid action"}')

        except Exception as e:
            logging.error(f"Error handling client: {e}")
            client_socket.send(b'{"error": "Internal server error"}')
        finally:
            client_socket.close()

    def store_data(self, identifier: str, data: bytes):
        """
        Stores data in the holographic storage.

        Args:
            identifier (str): A unique identifier for the data.
            data (bytes): The data to store.
        """
        success = self.storage.store_data(identifier, data)
        if success:
            logging.info(f"Data stored successfully with identifier '{identifier}'.")
        else:
            logging.warning(f"Failed to store data with identifier '{identifier}'.")

    def retrieve_data(self, identifier: str, client_socket):
        """
        Retrieves data from the holographic storage and sends it to the client.

        Args:
            identifier (str): The unique identifier for the data.
            client_socket (socket.socket): The socket object for the connected client.
        """
        data = self.storage.retrieve_data(identifier)
        if data is not None:
            client_socket.send(data)
            logging.info(f"Data retrieved successfully for identifier '{identifier}'.")
        else:
            logging.warning(f"No data found for identifier '{identifier}'.")
            client_socket.send(b'{"error": "Data not found"}')

    def stop_server(self):
        """
        Stops the edge computing server.
        """
        if self.server_socket:
            self.server_socket.close()
            logging.info("Edge computing server stopped.")
