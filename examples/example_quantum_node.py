# examples/example_quantum_node.py

import asyncio
from quantum_processing.quantum_node import QuantumNode

async def main():
    # Create a Quantum Node
    quantum_node = QuantumNode("QuantumNode1")

    # Prepare a quantum state
    state_vector = [0.707, 0.707]  # Example state for |+> (superposition)
    print(f"{quantum_node.node_id} is preparing a quantum state...")
    result = await quantum_node.prepare_state(state_vector)

    # Simulate sending quantum data to another node
    quantum_data = {"state": "superposition", "amplitudes": state_vector}
    print(f"{quantum_node.node_id} is sending quantum data...")
    await quantum_node.send_quantum_data("ReceiverNode", quantum_data)

    # Simulate receiving quantum data
    print(f"{quantum_node.node_id} is ready to receive quantum data.")
    await quantum_node.receive_quantum_data(quantum_data)

if __name__ == "__main__":
    asyncio.run(main())
