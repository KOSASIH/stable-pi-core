import hashlib
import time
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProofOfWork:
    def __init__(self, initial_difficulty: int = 4, adjustment_interval: int = 10):
        self.difficulty = initial_difficulty
        self.adjustment_interval = adjustment_interval
        self.block_times = []  # To track the time taken to mine blocks

    def mine(self, previous_nonce: int, block_data: str, miner_address: str, reward: float) -> int:
        """Perform the mining process to find a valid nonce and create a new block."""
        nonce = 0
        logging.info("Mining in progress...")
        start_time = time.time()

        while not self.valid_proof(previous_nonce, nonce, block_data):
            nonce += 1

        elapsed_time = time.time() - start_time
        self.block_times.append(elapsed_time)
        self.adjust_difficulty()  # Adjust difficulty based on recent block times

        logging.info(f"Mining completed in {elapsed_time:.2f} seconds with nonce: {nonce}")
        logging.info(f"Mining reward of {reward} awarded to {miner_address}")
        return nonce

    def valid_proof(self, previous_nonce: int, nonce: int, block_data: str) -> bool:
        """Check if the proof of work is valid."""
        guess = f"{previous_nonce}{nonce}{block_data}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:self.difficulty] == "0" * self.difficulty  # Adjusted difficulty

    def adjust_difficulty(self):
        """Adjust the mining difficulty based on the average time taken to mine recent blocks."""
        if len(self.block_times) < self.adjustment_interval:
            return  # Not enough data to adjust difficulty

        average_time = sum(self.block_times[-self.adjustment_interval:]) / self.adjustment_interval
        logging.info(f"Average mining time for last {self.adjustment_interval} blocks: {average_time:.2f} seconds")

        # Adjust difficulty based on average time
        if average_time < 2:  # If blocks are mined too quickly
            self.difficulty += 1
            logging.info("Increasing difficulty to: {}".format(self.difficulty))
        elif average_time > 5:  # If blocks are mined too slowly
            self.difficulty = max(1, self.difficulty - 1)  # Ensure difficulty doesn't go below 1
            logging.info("Decreasing difficulty to: {}".format(self.difficulty))

# Example usage
if __name__ == "__main__":
    pow = ProofOfWork(initial_difficulty=4)
    previous_nonce = 0
    block_data = "Sample block data"
    miner_address = "MinerPublicKey"
    reward = 50.0  # Example mining reward

    nonce = pow.mine(previous_nonce, block_data, miner_address, reward)
    print(f"Valid nonce found: {nonce}, Difficulty: {pow.difficulty}")
