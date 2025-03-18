# core/quantum_gravitational_consensus.py

import logging
import random
import time
from threading import Lock, Thread
from collections import Counter

# Configure logging for Quantum Gravitational Consensus
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuantumGravitationalConsensus:
    """
    Implements a consensus algorithm for quantum gravity sensors in a distributed network.
    """

    def __init__(self, node_id, total_nodes, timeout=5):
        """
        Initialize the Quantum Gravitational Consensus instance.

        :param node_id: Unique identifier for the node.
        :param total_nodes: Total number of nodes in the network.
        :param timeout: Timeout for waiting for responses.
        """
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.timeout = timeout
        self.lock = Lock()
        self.votes = {}
        self.proposed_value = None
        logger.info("Quantum Gravitational Consensus initialized for node %s", self.node_id)

    def propose_value(self, value):
        """
        Propose a value to the network and initiate the consensus process.

        :param value: The value to propose.
        :return: The agreed value after consensus.
        """
        self.proposed_value = value
        logger.info("Node %s proposing value: %s", self.node_id, value)
        self.votes[self.node_id] = value
        self.broadcast_proposal(value)

        # Wait for votes from other nodes
        time.sleep(self.timeout)

        agreed_value = self.decide_value()
        logger.info("Node %s agreed on value: %s", self.node_id, agreed_value)
        return agreed_value

    def broadcast_proposal(self, value):
        """
        Simulate broadcasting the proposed value to other nodes.

        :param value: The proposed value.
        """
        logger.info("Node %s broadcasting proposal: %s", self.node_id, value)
        threads = []
        for node in range(self.total_nodes):
            if node != self.node_id:
                thread = Thread(target=self.simulate_vote, args=(node, value))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()  # Wait for all threads to finish

    def simulate_vote(self, node, value):
        """
        Simulate receiving a vote from another node.

        :param node: The ID of the node voting.
        :param value: The proposed value.
        """
        # Simulate network delay
        time.sleep(random.uniform(0.1, 0.5))
        logger.info("Node %s received vote from Node %s: %s", self.node_id, node, value)
        with self.lock:
            self.votes[node] = value

    def decide_value(self):
        """
        Decide the final value based on the votes received.

        :return: The agreed value.
        """
        if len(self.votes) < (self.total_nodes / 2):
            logger.warning("Not enough votes received. Current votes: %s", self.votes)
            return None

        # Count votes
        vote_count = Counter(self.votes.values())
        logger.info("Votes counted: %s", vote_count)

        # Determine the value with the majority
        agreed_value, count = vote_count.most_common(1)[0]
        if count > (self.total_nodes / 2):
            logger.info("Majority value agreed upon: %s with %d votes", agreed_value, count)
            return agreed_value
        else:
            logger.warning("No majority found. Current votes: %s", self.votes)
            return None

# Example usage
if __name__ == "__main__":
    total_nodes = 5
    node_id = random.randint(0, total_nodes - 1)
    consensus = QuantumGravitationalConsensus(node_id=node_id, total_nodes=total_nodes)

    # Propose a value
    proposed_value = random.uniform(9.5, 10.5)  # Simulated gravity value
    agreed_value = consensus.propose_value(proposed_value)
    print(f"Node {node_id} agreed on value: {agreed_value:.4f}")
