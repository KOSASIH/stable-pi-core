import time
import json

class CosmicEntropyReversalEngine:
    def __init__(self):
        self.entropy_levels = {}
        self.entropy_log = []

    def monitor_entropy(self, node_id, level):
        """Monitor and record the entropy level for a node."""
        self.entropy_levels[node_id] = level
        self.log_entropy(node_id, level)
        print(f"Monitoring entropy level {level} for node {node_id}.")

    def log_entropy(self, node_id, level):
        """Log the entropy level change."""
        timestamp = time.time()
        entry = {
            'node_id': node_id,
            'level': level,
            'timestamp': timestamp
        }
        self.entropy_log.append(entry)
        print(f"Entropy logged: {json.dumps(entry)}")

    def reverse_entropy(self, node_id):
        """Reverse the entropy for a monitored node."""
        if node_id not in self.entropy_levels:
            raise ValueError(f"Node {node_id} is not being monitored.")
        
        current_level = self.entropy_levels[node_id]
        if current_level > 0:
            new_level = max(0, current_level - 1)  # Reverse entropy by reducing the level
            self.entropy_levels[node_id] = new_level
            self.log_reversal(node_id, current_level, new_level)
            print(f"Reversed entropy for node {node_id}. New level: {new_level}.")
        else:
            print(f"Entropy for node {node_id} is already at minimum level.")

    def log_reversal(self, node_id, old_level, new_level):
        """Log the entropy reversal action."""
        timestamp = time.time()
        reversal_entry = {
            'node_id': node_id,
            'old_level': old_level,
            'new_level': new_level,
            'timestamp': timestamp
        }
        print(f"Entropy reversal logged: {json.dumps(reversal_entry)}")

    def get_entropy_levels(self):
        """Retrieve the current entropy levels of all monitored nodes."""
        return self.entropy_levels

    def get_entropy_log(self):
        """Retrieve the log of all entropy levels and reversals."""
        return self.entropy_log

# Example usage
if __name__ == "__main__":
    cere = CosmicEntropyReversalEngine()
    try:
        cere.monitor_entropy("Node_A", 5)
        cere.monitor_entropy("Node_B", 3)

        cere.reverse_entropy("Node_A")
        cere.reverse_entropy("Node_B")
        cere.reverse_entropy("Node_B")  # Reverse again

        print("Current Entropy Levels:", cere.get_entropy_levels())
        print("Entropy Log:", cere.get_entropy_log())

        # Attempt to reverse entropy for a non-monitored node
        cere.reverse_entropy("Node_C")  # This should raise an error

    except Exception as e:
        print(f"Error: {e}")
