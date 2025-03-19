# simulations/performance_tests.py

import asyncio
import time
import logging
from quantum_processing.quantum_node import QuantumNode
from quantum_processing.quantum_protocol import QuantumProtocol

# Configure logging for performance tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceTest:
    def __init__(self, num_tests=10):
        self.num_tests = num_tests
        self.quantum_protocol = QuantumProtocol()
        self.sender_node = QuantumNode("SenderNode")
        self.receiver_node = QuantumNode("ReceiverNode")

    async def run_test(self):
        """Run a performance test for quantum communication."""
        logger.info("Starting performance tests...")
        total_time = 0

        for i in range(self.num_tests):
            quantum_state = {"state": "superposition", "amplitudes": [0.707, 0.707]}  # Example quantum state
            start_time = time.time()

            # Create a quantum message
            message = self.quantum_protocol.create_message("SenderNode", "ReceiverNode", quantum_state)

            # Simulate sending the message
            await self.sender_node.send_quantum_data(self.receiver_node, message)

            end_time = time.time()
            elapsed_time = end_time - start_time
            total_time += elapsed_time
            logger.info(f"Test {i + 1}: Elapsed time for communication: {elapsed_time:.6f} seconds")

        average_time = total_time / self.num_tests
        logger.info(f"Average time for {self.num_tests} tests: {average_time:.6f} seconds")

    async def run(self):
        """Run the performance test."""
        await self.run_test()

if __name__ == "__main__":
    performance_test = PerformanceTest(num_tests=10)
    try:
        asyncio.run(performance_test.run())
    except KeyboardInterrupt:
        logger.info("Performance testing stopped.")
