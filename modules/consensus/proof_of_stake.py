import random
import logging
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProofOfStake:
    def __init__(self):
        self.stakes = defaultdict(float)  # Dictionary to hold stakes of each validator
        self.total_stake = 0.0  # Total stake in the network

    def register_stake(self, validator: str, amount: float):
        """Register or update a stake for a validator."""
        if amount <= 0:
            logging.error("Stake amount must be positive.")
            return

        self.stakes[validator] += amount
        self.total_stake += amount
        logging.info(f"Stake registered: {validator} -> {self.stakes[validator]}")

    def select_validator(self) -> str:
        """Select a validator based on their stake using weighted random selection."""
        if self.total_stake == 0:
            logging.warning("No stakes registered.")
            return None

        selection = random.uniform(0, self.total_stake)
        current = 0
        for validator, stake in self.stakes.items():
            current += stake
            if current >= selection:
                logging.info(f"Validator selected: {validator} with stake: {stake}")
                return validator

    def distribute_rewards(self, validator: str, reward: float):
        """Distribute rewards to the selected validator."""
        if validator in self.stakes:
            self.stakes[validator] += reward
            logging.info(f"Reward of {reward} distributed to {validator}. New stake: {self.stakes[validator]}")
        else:
            logging.error(f"Validator {validator} not found for reward distribution.")

    def get_stake(self, validator: str) -> float:
        """Get the stake of a specific validator."""
        return self.stakes[validator]

    def __repr__(self) -> str:
        return f"ProofOfStake(stakes={dict(self.stakes)}, total_stake={self.total_stake})"

# Example usage
if __name__ == "__main__":
    pos = ProofOfStake()
    pos.register_stake("Alice", 50)
    pos.register_stake("Bob", 30)
    pos.register_stake("Charlie", 20)

    selected_validator = pos.select_validator()
    if selected_validator:
        print(f"Selected Validator: {selected_validator}")
        pos.distribute_rewards(selected_validator, 10)  # Example reward distribution
