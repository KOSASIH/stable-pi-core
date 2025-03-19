# quantum_network/node.py

import random
import numpy as np

class QuantumNode:
    def __init__(self, node_id):
        """
        Initialize a Quantum Node.

        Args:
            node_id (str): Unique identifier for the quantum node.
        """
        self.node_id = node_id
        self.entangled_pairs = []  # List to store entangled qubit pairs
        self.state = None           # Current state of the node

    def create_entangled_pair(self):
        """
        Create a pair of entangled qubits and store them in the node.

        Returns:
            tuple: A tuple representing the entangled qubit pair.
        """
        # Simulate the creation of entangled qubits (using Bell states)
        qubit_a = np.array([1, 0])  # |0>
        qubit_b = np.array([0, 1])  # |1>
        
        # Create a Bell state (|00> + |11>) / sqrt(2)
        entangled_pair = (qubit_a + qubit_b) / np.sqrt(2)
        self.entangled_pairs.append(entangled_pair)
        print(f"{self.node_id}: Created entangled pair {entangled_pair}")
        return entangled_pair

    def send_message(self, message, target_node):
        """
        Send a message to another quantum node using quantum communication.

        Args:
            message (str): The message to send.
            target_node (QuantumNode): The target quantum node to send the message to.
        """
        if not self.entangled_pairs:
            print(f"{self.node_id}: No entangled pairs available to send messages.")
            return
        
        # Simulate quantum communication (for simplicity, we just print the message)
        print(f"{self.node_id}: Sending message '{message}' to {target_node.node_id} using quantum communication.")
        
        # Here you would implement the actual quantum communication logic
        # For example, using quantum teleportation or QKD (Quantum Key Distribution)
        target_node.receive_message(message)

    def receive_message(self, message):
        """
        Receive a message from another quantum node.

        Args:
            message (str): The received message.
        """
        print(f"{self.node_id}: Received message '{message}'.")

    def measure_qubit(self, qubit):
        """
        Measure a qubit and collapse its state.

        Args:
            qubit (np.array): The qubit to measure.

        Returns:
            int: The measurement result (0 or 1).
        """
        probabilities = np.abs(qubit) ** 2
        result = np.random.choice([0, 1], p=probabilities)
        print(f"{self.node_id}: Measured qubit with result {result}.")
        return result

    def __str__(self):
        return f"QuantumNode({self.node_id})"

# Example usage
if __name__ == "__main__":
    node_a = QuantumNode("Node_A")
    node_b = QuantumNode("Node_B")

    # Create entangled pairs
    node_a.create_entangled_pair()
    node_b.create_entangled_pair()

    # Send a message
    node_a.send_message("Hello, Node B!", node_b)
