import time
import json

class EternalChronoStabilizer:
    def __init__(self):
        self.time_stamps = {}

    def record_transaction(self, transaction_id, user_id, asset, amount):
        """Record a transaction with temporal integrity."""
        if transaction_id in self.time_stamps:
            raise ValueError(f"Transaction ID {transaction_id} already exists.")
        
        timestamp = time.time()
        self.time_stamps[transaction_id] = {
            'user_id': user_id,
            'asset': asset,
            'amount': amount,
            'timestamp': timestamp
        }
        print(f"Transaction {transaction_id} recorded with temporal integrity at {self.format_timestamp(timestamp)}.")

    def format_timestamp(self, timestamp):
        """Format the timestamp into a human-readable format."""
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

    def verify_transaction(self, transaction_id):
        """Verify the integrity of a recorded transaction."""
        if transaction_id in self.time_stamps:
            transaction = self.time_stamps[transaction_id]
            print(f"Transaction {transaction_id} verified: {json.dumps(transaction)}")
            return True
        else:
            print(f"Transaction {transaction_id} not found.")
            return False

    def get_transaction_history(self):
        """Retrieve the history of recorded transactions."""
        return self.time_stamps

    def simulate_time_dilation(self, factor):
        """Simulate time dilation effects for educational purposes."""
        if factor <= 0:
            raise ValueError("Time dilation factor must be greater than zero.")
        simulated_time = time.time() * factor
        print(f"Simulated time dilation factor {factor}: {self.format_timestamp(simulated_time)}")
        return simulated_time

# Example usage
if __name__ == "__main__":
    ecs = EternalChronoStabilizer()
    try:
        ecs.record_transaction("tx_001", "User _1", "CNC", 100)
        ecs.record_transaction("tx_002", "User _2", "CNC", 50)

        ecs.verify_transaction("tx_001")
        ecs.verify_transaction("tx_003")  # This should fail

        print("Transaction History:", ecs.get_transaction_history())

        # Simulate time dilation
        ecs.simulate_time_dilation(2)  # Simulate time at twice the normal rate

    except Exception as e:
        print(f"Error: {e}")
