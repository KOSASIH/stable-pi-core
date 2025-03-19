import threading
import time
import argparse
from energy_harvester import EnergyHarvester

class EnergyMonitor:
    def __init__(self, harvester):
        self.harvester = harvester
        self.running = True

    def display_status(self):
        """
        Display the current status of the energy harvester in real-time.
        """
        while self.running:
            total_energy = self.harvester.get_total_energy()
            print(f"\rTotal Energy Collected: {total_energy:.2f} Joules", end="")
            time.sleep(1)

    def stop(self):
        self.running = False

def main(harvesting_rate, efficiency):
    print("Initializing Zero-Point Energy Harvesting Module...")
    harvester = EnergyHarvester(base_efficiency=efficiency)
    harvester.harvesting_rate = harvesting_rate

    # Start the energy monitoring in a separate thread
    monitor = EnergyMonitor(harvester)
    monitor_thread = threading.Thread(target=monitor.display_status)
    monitor_thread.start()

    try:
        while True:
            harvested_energy = harvester.harvest_energy()
            # Simulate energy distribution to external systems
            if harvested_energy > 0.5:  # Example condition for distribution
                harvester.distribute_energy(0.5)
            time.sleep(1)  # Simulate time delay for harvesting
    except KeyboardInterrupt:
        print("\nStopping energy harvesting...")
    finally:
        monitor.stop()
        monitor_thread.join()
        print(f"\nTotal Energy Collected: {harvester.get_total_energy():.2f} Joules")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zero-Point Energy Harvesting Module")
    parser.add_argument('--harvesting_rate', type=float, default=1.0,
                        help='Rate of energy harvesting (Joules per second)')
    parser.add_argument('--efficiency', type=float, default=0.85,
                        help='Base efficiency of the energy harvesting process (0 to 1)')
    args = parser.parse_args()

    main(args.harvesting_rate, args.efficiency)
