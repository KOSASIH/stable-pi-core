import time
import logging
import threading
from energy_harvester import EnergyHarvester
from quantum_interface import QuantumInterface

# Configure logging
logging.basicConfig(filename='stable_pi_core.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class StablePiCore:
    def __init__(self, harvesting_rate=1.0, efficiency=0.85):
        """
        Initialize the Stable-Pi-Core system with energy harvesting and quantum interface.
        
        :param harvesting_rate: Rate of energy harvesting (Joules per second).
        :param efficiency: Base efficiency of the energy harvesting process (0 to 1).
        """
        self.harvester = EnergyHarvester(base_efficiency=efficiency)
        self.quantum_interface = QuantumInterface()
        self.energy_nodes = []  # List to hold connected energy nodes
        self.running = True
        logging.info("Stable-Pi-Core initialized.")

    def add_node(self, node_name):
        """
        Add a new energy node to the system.
        
        :param node_name: Name of the node to be added.
        """
        self.energy_nodes.append(node_name)
        logging.info(f"Node {node_name} added to Stable-Pi-Core.")

    def harvest_energy(self):
        """
        Harvest energy and log the results.
        """
        harvested_energy = self.harvester.harvest_energy()
        logging.info(f"Harvested Energy: {harvested_energy:.2f} Joules")
        return harvested_energy

    def distribute_energy(self, amount):
        """
        Distribute energy to connected nodes if sufficient energy is available.
        
        :param amount: Amount of energy to distribute in Joules.
        """
        if self.harvester.get_total_energy() >= amount:
            for node in self.energy_nodes:
                logging.info(f"Distributing {amount:.2f} Joules to node {node}.")
            self.harvester.distribute_energy(amount)
        else:
            logging.warning("Insufficient energy to distribute.")

    def monitor_system(self):
        """
        Monitor the system and log energy metrics.
        """
        while self.running:
            total_energy = self.harvester.get_total_energy()
            logging.info(f"Total Energy Collected: {total_energy:.2f} Joules")
            time.sleep(5)  # Log every 5 seconds

    def run(self):
        """
        Main loop to run the Stable-Pi-Core system.
        """
        try:
            while self.running:
                harvested_energy = self.harvest_energy()
                self.distribute_energy(1.0)  # Example: distribute 1 Joule
                time.sleep(1)  # Harvest energy every second
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            self.shutdown()

    def shutdown(self):
        """
        Gracefully shut down the system.
        """
        self.running = False
        logging.info("Shutting down Stable-Pi-Core.")
        total_energy = self.harvester.get_total_energy()
        logging.info(f"Final Total Energy Collected: {total_energy:.2f} Joules")

if __name__ == "__main__":
    stable_pi_core = StablePiCore(harvesting_rate=1.0, efficiency=0.90)
    stable_pi_core.add_node("Node_A")
    stable_pi_core.add_node("Node_B")

    # Start monitoring in a separate thread
    monitoring_thread = threading.Thread(target=stable_pi_core.monitor_system)
    monitoring_thread.start()

    stable_pi_core.run()

    # Wait for the monitoring thread to finish
    monitoring_thread.join()
