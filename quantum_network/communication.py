# quantum_network/communication.py

import numpy as np
from .node import QuantumNode

class QuantumCommunication:
    def __init__(self):
        """
        Initialize the Quantum Communication Protocols.
        """
        pass

    @staticmethod
    def quantum_teleportation(sender: QuantumNode, receiver: QuantumNode, message: str):
        """
        Simulate quantum teleportation of a message from sender to receiver.

        Args:
            sender (QuantumNode): The sender node.
            receiver (QuantumNode): The receiver node.
            message (str): The message to teleport.
        """
        print(f"{sender.node_id}: Preparing to teleport message '{message}' to {receiver.node_id}.")

        # Create entangled pairs if not already available
        if not sender.entangled_pairs:
            sender.create_entangled_pair()
        if not receiver.entangled_pairs:
            receiver.create_entangled_pair()

        # Simulate the encoding of the message into a qubit
        message_qubit = QuantumCommunication.encode_message(message)

        # Simulate the teleportation process
        print(f"{sender.node_id}: Teleporting message '{message}'...")
        sender.measure_qubit(message_qubit)  # Measure the message qubit
        receiver.receive_message(message)      # Directly send the message for simplicity

    @staticmethod
    def encode_message(message: str) -> np.ndarray:
        """
        Encode a message into a qubit representation.

        Args:
            message (str): The message to encode.

        Returns:
            np.ndarray: The encoded qubit.
        """
        # For simplicity, we will represent the message as a binary string
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        qubit = np.array([0, 0], dtype=complex)

        # Simple encoding: set the qubit based on the first character
        if binary_message:
            qubit[0] = 1 if binary_message[0] == '1' else 0
            qubit[1] = 1 if binary_message[0] == '0' else 0

        print(f"Encoded message '{message}' into qubit {qubit}.")
        return qubit

    @staticmethod
    def quantum_key_distribution(sender: QuantumNode, receiver: QuantumNode):
        """
        Simulate a simple Quantum Key Distribution (QKD) process.

        Args:
            sender (QuantumNode): The sender node.
            receiver (QuantumNode): The receiver node.
        """
        print(f"{sender.node_id}: Starting Quantum Key Distribution with {receiver.node_id}.")

        # Create entangled pairs
        sender.create_entangled_pair()
        receiver.create_entangled_pair()

        # Simulate the generation of a shared secret key
        key = np.random.randint(0, 2, size=8)  # Generate an 8-bit key
        print(f"{sender.node_id}: Generated secret key {key}.")

        # Simulate the transmission of the key
        print(f"{sender.node_id}: Sending key to {receiver.node_id}...")
        receiver.receive_message(f"Shared key: {key}")

    @staticmethod
    def receive_message(receiver: QuantumNode, message: str):
        """
        Handle the reception of a message at the receiver node.

        Args:
            receiver (QuantumNode): The receiver node.
            message (str): The received message.
        """
        print(f"{receiver.node_id}: Received message '{message}'.")

# Example usage
if __name__ == "__main__":
    node_a = QuantumNode("Node_A")
    node_b = QuantumNode("Node_B")

    # Simulate quantum teleportation
    QuantumCommunication.quantum_teleportation(node_a, node_b, "Hello, Node B!")

    # Simulate Quantum Key Distribution
    QuantumCommunication.quantum_key_distribution(node_a, node_b)
