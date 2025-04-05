import time
import json

class OmniGalacticResourceSymbiote:
    def __init__(self):
        self.resources = {}
        self.conversion_log = []

    def convert_energy(self, source, amount, efficiency=1.0):
        """Convert energy from a source into usable resources."""
        if amount < 0:
            raise ValueError("Amount of energy to convert must be non-negative.")
        
        converted_amount = amount * efficiency
        self.resources[source] = self.resources.get(source, 0) + converted_amount
        self.log_conversion(source, amount, converted_amount, efficiency)
        print(f"Converted {amount} energy from {source} into {converted_amount} usable resources.")

    def log_conversion(self, source, original_amount, converted_amount, efficiency):
        """Log the energy conversion details."""
        timestamp = time.time()
        entry = {
            'source': source,
            'original_amount': original_amount,
            'converted_amount': converted_amount,
            'efficiency': efficiency,
            'timestamp': timestamp
        }
        self.conversion_log.append(entry)
        print(f"Conversion logged: {json.dumps(entry)}")

    def allocate_resources(self, project, amount):
        """Allocate resources to a specific project."""
        if amount < 0:
            raise ValueError("Amount to allocate must be non-negative.")
        
        total_resources = sum(self.resources.values())
        if amount > total_resources:
            raise ValueError("Insufficient resources available for allocation.")
        
        # Deduct allocated resources from the total
        for source in list(self.resources.keys()):
            if self.resources[source] >= amount:
                self.resources[source] -= amount
                print(f"Allocated {amount} resources from {source} to project '{project}'.")
                return
            else:
                amount -= self.resources[source]
                self.resources[source] = 0
        
        print(f"Allocated resources to project '{project}'.")

    def get_resources(self):
        """Retrieve the current resources."""
        return self.resources

    def get_conversion_log(self):
        """Retrieve the log of all conversions."""
        return self.conversion_log

# Example usage
if __name__ == "__main__":
    ogrs = OmniGalacticResourceSymbiote()
    try:
        ogrs.convert_energy("Solar Panel", 100, efficiency=0.9)
        ogrs.convert_energy("Nuclear Reactor", 200, efficiency=0.85)

        print("Current Resources:", ogrs.get_resources())

        ogrs.allocate_resources("Project Alpha", 150)
        print("Current Resources after allocation:", ogrs.get_resources())

        print("Conversion Log:", ogrs.get_conversion_log())

        # Attempt to allocate more resources than available
        ogrs.allocate_resources("Project Beta", 300)  # This should raise an error

    except Exception as e:
        print(f"Error: {e}")
