import time
import numpy as np
from energy_harvester import EnergyHarvester
from quantum_interface import QuantumInterface

def main():
    # Initialize the Energy Harvester
    harvester = EnergyHarvester(base_efficiency=0.90)
    
    # Initialize the Quantum Interface
    quantum_interface = QuantumInterface()

    # Prepare a quantum state
    state_vector = [1/np.sqrt(2), 1/np.sqrt(2)]  # Example: |+> state
    quantum_interface.prepare_quantum_state(state_vector)

    try:
        print("Starting energy harvesting...")
        for _ in range(10):  # Harvest energy for 10 seconds
            harvested_energy = harvester.harvest_energy()
            print(f"Harvested Energy: {harvested_energy:.2f} Joules")
            time.sleep(1)  # Simulate time delay for harvesting

            # Measure the quantum state
            measurement_result = quantum_interface.measure_quantum_state()
            print(f"Quantum Measurement Result: {measurement_result}")

            # Distribute some energy if enough is harvested
            if harvested_energy > 0.5:
                if harvester.distribute_energy(0.5):
                    print("Distributed 0.5 Joules of energy.")
                else:
                    print("Insufficient energy to distribute.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        total_energy = harvester.get_total_energy()
        print(f"Total Energy Collected: {total_energy:.2f} Joules")
        quantum_interface.reset_quantum_state()

if __name__ == "__main__":
    main()
