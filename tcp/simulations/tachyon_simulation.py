# simulations/tachyon_simulation.py

import asyncio
import logging
from tcp.main import TCPApplication
from quantum_processing.quantum_node import QuantumNode
from quantum_processing.quantum_protocol import QuantumProtocol
from tcp.data_packet import DataPacket

# Configure logging for the simulation
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TachyonSimulation:
    def __init__(self):
        self.tcp_app = TCPApplication()
        self.quantum_protocol = QuantumProtocol()
        self.nodes = {}

    async def add_quantum_node(self, node_id):
        """Add a quantum node to the simulation."""
        node = QuantumNode(node_id)
        self.nodes[node_id] = node
        logger.info(f"Added Quantum Node: {node_id}")

    async def simulate_communication(self, sender_id, receiver_id, quantum_state):
        """Simulate communication between two quantum nodes."""
        logger.info(f"Simulating communication from {sender_id} to {receiver_id} with quantum state: {quantum_state}")
        
        # Create a quantum message
        message = self.quantum_protocol.create_message(sender_id, receiver_id, quantum_state)
        
        # Simulate sending the message
        await self.nodes[sender_id].send_quantum_data(self.nodes[receiver_id], message)

    async def run_simulation(self):
        """Run the simulation."""
        await self.add_quantum_node("QuantumNode1")
        await self.add_quantum_node("QuantumNode2")

        # Prepare a quantum state for communication
        quantum_state = {"state": "superposition", "amplitudes": [0.707, 0.707]}  # Example quantum state

        # Simulate communication
        await self.simulate_communication("QuantumNode1", "QuantumNode2", quantum_state)

        # Keep the simulation running
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    simulation = TachyonSimulation()
    try:
        asyncio.run(simulation.run_simulation())
    except KeyboardInterrupt:
        logger.info("Tachyon Simulation stopped.")
