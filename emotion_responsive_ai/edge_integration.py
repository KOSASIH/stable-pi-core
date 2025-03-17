import socket
import threading
import logging
import numpy as np
import cv2
from emotion_detection import EmotionDetection

class EdgeIntegration:
    """
    A class to integrate edge computing with emotion detection.

    Attributes:
        host (str): The host address for the edge server.
        port (int): The port number for the edge server.
        emotion_detector (EmotionDetection): An instance of the emotion detection class.
    """

    def __init__(self, host='0.0.0.0', port=5000):
        """
        Initializes the EdgeIntegration instance.

        Args:
            host (str): The host address for the edge server.
            port (int): The port number for the edge server.
        """
        self.host = host
        self.port = port
        self.emotion_detector = EmotionDetection()  # Initialize the emotion detector
        logging.info(f"Edge Integration initialized on {self.host}:{self.port}")

    def start_server(self):
        """Starts the edge computing server to listen for incoming data."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        logging.info("Edge server started, waiting for connections...")

        while True:
            client_socket, addr = server_socket.accept()
            logging.info(f"Connection from {addr} established.")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        """Handles communication with a connected client."""
        try:
            while True:
                # Receive data from the client
                data = client_socket.recv(4096)
                if not data:
                    break

                # Process the received data (assumed to be an image)
                frame = self.process_received_data(data)

                # Detect emotions from the frame
                emotions = self.emotion_detector.detect_emotion(frame)

                # Send the detected emotions back to the client
                response = self.create_response(emotions)
                client_socket.sendall(response.encode('utf-8'))

        except Exception as e:
            logging.error(f"Error handling client: {e}")
        finally:
            client_socket.close()
            logging.info("Client connection closed.")

    def process_received_data(self, data):
        """Processes the received data into a format suitable for emotion detection."""
        # Convert the received data into a NumPy array (assuming it's an image)
        nparr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return frame

    def create_response(self, emotions):
        """Creates a response string from the detected emotions."""
        response = ', '.join([f"{emotion}: {confidence:.2f}" for emotion, confidence in emotions.items()])
        return response

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    edge_integration = EdgeIntegration()
    edge_integration.start_server()
