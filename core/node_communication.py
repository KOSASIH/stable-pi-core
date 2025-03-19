# core/node_communication.py

import logging
import socket
import json
import threading
import time

# Configure logging for Node Communication
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NodeCommunication:
    """
    Manages communication between nodes in the network.
    """

    def __init__(self, host='localhost', port=5000):
        """
        Initialize the NodeCommunication instance.

        :param host: Host address for the node.
        :param port: Port number for the node.
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_sockets = []
        self.lock = threading.Lock()
        logger.info("NodeCommunication initialized on %s:%d", self.host, self.port)

    def start_server(self):
        """
        Start the server to listen for incoming connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        logger.info("Server started, waiting for connections...")

        while True:
            client_socket, address = self.server_socket.accept()
            logger.info("Connection established with %s", address)
            self.client_sockets.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        """
        Handle communication with a connected client.

        :param client_socket: The socket object for the connected client.
        """
        with client_socket:
            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        logger.info("Client disconnected.")
                        break
                    message = json.loads(data.decode('utf-8'))
                    logger.info("Received message: %s", message)
                    self.process_message(message, client_socket)
                except json.JSONDecodeError:
                    logger.error("Received invalid JSON data.")
                    break
                except Exception as e:
                    logger.error("Error handling client: %s", e)
                    break

    def process_message(self, message, client_socket):
        """
        Process the received message and respond if necessary.

        :param message: The message received from the client.
        :param client_socket: The socket object for the client.
        """
        # Example processing logic
        response = {"status": "received", "data": message}
        self.send_message(response, client_socket)

    def send_message(self, message, client_socket):
        """
        Send a message to a connected client.

        :param message: The message to send (dict).
        :param client_socket: The socket object for the client.
        """
        try:
            message_json = json.dumps(message).encode('utf-8')
            client_socket.sendall(message_json)
            logger.info("Sent message: %s", message)
        except Exception as e:
            logger.error("Error sending message: %s", e)

    def connect_to_node(self, host, port):
        """
        Connect to another node in the network.

        :param host: Host address of the node to connect to.
        :param port: Port number of the node to connect to.
        """
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            logger.info("Connected to node %s:%d", host, port)
            self.client_sockets.append(client_socket)
            return client_socket
        except Exception as e:
            logger.error("Failed to connect to node %s:%d: %s", host, port, e)
            return None

    def close_connections(self):
        """
        Close all active connections.
        """
        with self.lock:
            for client_socket in self.client_sockets:
                client_socket.close()
            self.client_sockets.clear()
            logger.info("All connections closed.")

    def broadcast_message(self, message):
        """
        Broadcast a message to all connected clients.

        :param message: The message to broadcast (dict).
        """
        with self.lock:
            for client_socket in self.client_sockets:
                self.send_message(message, client_socket)

# Example usage
if __name__ == "__main__":
    node_comm = NodeCommunication()
    
    # Start the server in a separate thread
    server_thread = threading.Thread(target=node_comm.start_server)
    server_thread.start()

    # Connect to another node (example)
    time.sleep (1)  # Wait for the server to start
    client_socket = node_comm.connect_to_node('localhost', 5001)

    # Example of sending a message
    if client_socket:
        node_comm.send_message({"message": "Hello from Node 1"}, client_socket)

    # Example of broadcasting a message
    time.sleep(2)  # Allow some time for connections
    node_comm.broadcast_message({"message": "Broadcasting to all nodes!"})

    # Close connections when done
    time.sleep(5)  # Keep the client alive for a while
    node_comm.close_connections()
