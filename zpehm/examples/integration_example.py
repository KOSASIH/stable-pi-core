import time
from energy_harvester import EnergyHarvester
from quantum_interface import QuantumInterface

class StablePiCore:
    def __init__(self):
        self.energy_nodes = []
    
    def add_node(self, node):
        self.energy_nodes.append(node)
        print(f"Node {node} added to Stable-Pi-Core.")

    def distribute_energy_to_nodes(self, amount):
        for node in self.energy_nodes:
            print(f"Distributing {amount:.2f} Joules to node {node}.")

def main():
    # Initialize the Energy Harvester
    harvester = EnergyHarvester(base_efficiency=0.85)
    
    # Initialize the Quantum Interface
    quantum_interface = QuantumInterface()

    # Prepare a quantum state
    state_vector = [1/np.sqrt(2), 1/np.sqrt(2)]  # Example: |+> state
    quantum_interface.prepare_quantum_state(state_vector)

    # Initialize the Stable-Pi-Core system
    stable_pi_core = StablePiCore()
    stable_pi_core.add_node("Node_A")
    stable_pi_core.add_node("Node_B")

    try:
        print("Starting energy harvesting...")
        for _ in range(10):  # Harvest energy for 10 seconds
            harvested_energy = harvester.harvest_energy()
            print(f"Harvested Energy: {harvested_energy:.2f} Joules")
            time.sleep(1)  # Simulate time delay for harvesting

            # Measure the quantum state
            measurement_result = quantum_interface.measure_quantum_state()
            print(f"Quantum Measurement Result: {measurement_result}")

            # Distribute energy to nodes if enough is harvested
            if harvested_energy > 1.0:
                stable_pi_core.distribute_energy_to_nodes(1.0)
                harvester.distribute_energy(1.0)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        total_energy = harvester.get_total_energy()
        print(f"Total Energy Collected: {total_energy:.2f} Joules")
        quantum_interface.reset_quantum_state()

if __name__ == "__main__":
    main()
