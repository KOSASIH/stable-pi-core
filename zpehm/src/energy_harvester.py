import random
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='energy_harvester.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class EnergyHarvester:
    def __init__(self, base_efficiency=0.85):
        """
        Initialize the Energy Harvester with a specified base efficiency.
        
        :param base_efficiency: Base efficiency of the energy harvesting process (0 to 1).
        """
        self.base_efficiency = base_efficiency
        self.dynamic_efficiency = base_efficiency
        self.energy_collected = 0.0  # in Joules
        self.harvesting_rate = 1.0  # Energy harvested per second in Joules

    def adjust_efficiency(self):
        """
        Dynamically adjust the efficiency based on simulated environmental conditions.
        """
        # Simulate environmental factors affecting efficiency
        environmental_factor = random.uniform(0.8, 1.2)  # Random factor between 0.8 and 1.2
        self.dynamic_efficiency = self.base_efficiency * environmental_factor
        logging.info(f"Dynamic Efficiency Adjusted: {self.dynamic_efficiency:.2f}")

    def harvest_energy(self):
        """
        Simulate the process of harvesting energy from zero-point energy.
        
        :return: Amount of energy harvested in Joules.
        """
        self.adjust_efficiency()
        harvested_energy = self.harvesting_rate * self.dynamic_efficiency
        self.energy_collected += harvested_energy
        logging.info(f"Harvested Energy: {harvested_energy:.2f} Joules (Total: {self.energy_collected:.2f} Joules)")
        return harvested_energy

    def get_total_energy(self):
        """
        Get the total energy collected so far.
        
        :return: Total energy collected in Joules.
        """
        return self.energy_collected

    def reset_energy(self):
        """
        Reset the energy collected to zero.
        """
        self.energy_collected = 0.0
        logging.info("Energy collection reset.")

    def distribute_energy(self, amount):
        """
        Simulate the distribution of harvested energy to external systems or nodes.
        
        :param amount: Amount of energy to distribute in Joules.
        """
        if amount > self.energy_collected:
            logging.warning("Insufficient energy to distribute.")
            return False
        self.energy_collected -= amount
        logging.info(f"Distributed {amount:.2f} Joules to external systems.")
        return True

if __name__ == "__main__":
    harvester = EnergyHarvester()
    try:
        while True:
            harvester.harvest_energy()
            time.sleep(1)  # Simulate time delay for harvesting
    except KeyboardInterrupt:
        logging.info("Energy harvesting stopped.")
        print(f"Total Energy Collected: {harvester.get_total_energy():.2f} Joules")
