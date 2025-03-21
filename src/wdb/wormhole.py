# wdb/wormhole.py

import asyncio
import random
import hashlib
from .logger import Logger
from .quantum_entanglement import QuantumEntanglement

class WormholeError(Exception):
    """Custom exception for Wormhole errors."""
    pass

class Wormhole:
    def __init__(self, node_a, node_b, latency_range=(0.1, 0.5)):
        self.node_a = node_a
        self.node_b = node_b
        self.latency_range = latency_range  # Latency range in seconds
        self.logger = Logger()
        self.quantum_entanglement = QuantumEntanglement()

    async def simulate_transfer(self, data):
        """
        Simulates the transfer of data through a wormhole with quantum entanglement.
        
        Args:
            data (str): The data to be transferred.

        Returns:
            str: The data after transfer.
        """
        self.logger.log(f"Preparing to transfer data from {self.node_a} to {self.node_b} via wormhole...")

        # Simulate quantum entanglement
        entangled_data = self.quantum_entanglement.entangle(data)

        # Simulate dynamic latency based on network conditions
        latency = random.uniform(*self.latency_range)  # Latency within the specified range
        self.logger.log(f"Simulating transfer with an estimated latency of {latency:.2f} seconds...")
        
        await asyncio.sleep(latency)  # Simulate the time taken for transfer

        self.logger.log(f"Transfer completed successfully from {self.node_a} to {self.node_b}.")
        return entangled_data  # Return the entangled data as the result of the transfer

    def validate_data(self, data):
        """
        Validates the data to ensure it meets the required criteria for transfer.
        
        Args:
            data (str): The data to be validated.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not isinstance(data, str) or len(data) == 0:
            self.logger.log("Data validation failed: Data must be a non-empty string.")
            return False
        self.logger.log("Data validation successful.")
        return True

    def calculate_checksum(self, data):
        """
        Calculates a checksum for the data to ensure integrity during transfer.
        
        Args:
            data (str): The data to calculate the checksum for.

        Returns:
            str: The checksum of the data.
        """
        checksum = hashlib.sha256(data.encode()).hexdigest()
        self.logger.log(f"Calculated checksum: {checksum}")
        return checksum

    async def transfer_data(self, data):
        """
        Initiates the data transfer process after validation.
        
        Args:
            data (str): The data to be transferred.

        Returns:
            str: The result of the transfer or an error message.
        """
        if self.validate_data(data):
            checksum = self.calculate_checksum(data)
            self.logger.log(f"Starting transfer with checksum: {checksum}")
            try:
                result = await self.simulate_transfer(data)
                self.logger.log(f"Transfer successful with checksum: {checksum}")
                return result
            except Exception as e:
                raise WormholeError(f"Transfer failed due to an error: {str(e)}")
        else:
            return "Transfer failed due to invalid data."
