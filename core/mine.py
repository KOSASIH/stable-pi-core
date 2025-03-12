import time
import logging
from transaction import Transaction
from block import Block
from blockchain import Blockchain

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Miner:
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain

    def mine(self) -> Block:
        # Ensure there are transactions to mine
        if not self.blockchain.current_transactions:
            logging.warning("No transactions to mine.")
            return None

        # Prepare the new block
        previous_block = self.blockchain.last_block
        index = previous_block.index + 1
        timestamp = time.time()
        transactions = self.blockchain.current_transactions[:]
        
        # Start mining
        nonce = self.proof_of_work(previous_block.nonce)
        new_block = Block(index=index, previous_hash=previous_block.hash, timestamp=timestamp, transactions=transactions, nonce=nonce)

        # Add the new block to the blockchain
        if new_block.is_valid():
            self.blockchain.create_block(nonce, previous_hash=previous_block.hash)
            logging.info(f"New block mined: {new_block.index} with hash: {new_block.hash}")
            return new_block
        else:
            logging.error("Failed to mine a valid block.")
            return None

    def proof_of_work(self, previous_nonce: int) -> int:
        nonce = 0
        logging.info("Mining in progress...")
        start_time = time.time()
        
        while not self.blockchain.valid_proof(previous_nonce, nonce):
            nonce += 1
        
        elapsed_time = time.time() - start_time
        logging.info(f"Mining completed in {elapsed_time:.2f} seconds with nonce: {nonce}")
        return nonce

# Example usage
if __name__ == "__main__":
    # Create a blockchain instance
    blockchain = Blockchain()

    # Create a miner instance
    miner = Miner(blockchain)

    # Simulate adding transactions
    transaction1 = Transaction(sender="AlicePublicKey", recipient="BobPublicKey", amount=50, signature="SampleSignature1")
    transaction2 = Transaction(sender="BobPublicKey", recipient="CharliePublicKey", amount=25, signature="SampleSignature2")

    # Add transactions to the blockchain
    blockchain.add_transaction(transaction1.sender, transaction1.recipient, transaction1.amount, transaction1.signature)
    blockchain.add_transaction(transaction2.sender, transaction2.recipient, transaction2.amount, transaction2.signature)

    # Mine a new block
    mined_block = miner.mine()

    # Print the mined block
    if mined_block:
        print(f"Mined Block: {mined_block.index}, Hash: {mined_block.hash}, Transactions: {mined_block.transactions}")
