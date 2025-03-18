# tcp/synchronization.py

import time
import logging
import asyncio

# Configure logging for Synchronization
logger = logging.getLogger(__name__)

class Synchronization:
    """Class for handling Space-Time Synchronization Protocol."""

    def __init__(self):
        self.time_offset = 0  # Time offset for synchronization
        self.local_time = self.get_current_time()
        logger.info("Space-Time Synchronization Protocol initialized.")

    def get_current_time(self):
        """Get the current UTC time in seconds since the epoch."""
        return time.time()

    def synchronize_with(self, remote_time):
        """Synchronize local time with remote time."""
        self.local_time = self.get_current_time()
        self.time_offset = remote_time - self.local_time
        logger.info(f"Synchronized with remote time. Time offset: {self.time_offset:.6f} seconds.")

    def get_synchronized_time(self):
        """Get the synchronized local time."""
        synchronized_time = self.get_current_time() + self.time_offset
        logger.debug(f"Synchronized time: {synchronized_time:.6f} seconds.")
        return synchronized_time

    async def periodic_sync(self, remote_node):
        """Periodically synchronize with a remote node."""
        while True:
            await asyncio.sleep(10)  # Synchronize every 10 seconds
            remote_time = await remote_node.request_time()
            self.synchronize_with(remote_time)

class RemoteNode:
    """Simulated remote node for demonstration purposes."""

    def __init__(self, node_id):
        self.node_id = node_id

    async def request_time(self):
        """Simulate a request for the current time from the remote node."""
        await asyncio.sleep(1)  # Simulate network delay
        current_time = time.time()  # Return the current time
        logger.info(f"Remote Node {self.node_id} responding with time: {current_time:.6f} seconds.")
        return current_time

# Example usage of the Synchronization class
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sync = Synchronization()
    remote_node = RemoteNode("Node2")

    # Start periodic synchronization
    try:
        asyncio.run(sync.periodic_sync(remote_node))
    except KeyboardInterrupt:
        logger.info("Synchronization process stopped.")
