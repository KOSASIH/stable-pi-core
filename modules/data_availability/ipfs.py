import ipfshttpclient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class IPFSStorage:
    def __init__(self):
        """Initialize IPFS client."""
        self.client = ipfshttpclient.connect()
        logging.info("Connected to IPFS")

    def add_file(self, file_path: str) -> str:
        """Add a file to IPFS and return its CID."""
        res = self.client.add(file_path)
        cid = res['Hash']
        logging.info(f"File added to IPFS with CID: {cid}")
        return cid

    def get_file(self, cid: str, output_path: str):
        """Retrieve a file from IPFS using its CID."""
        self.client.get(cid, target=output_path)
        logging.info(f"File retrieved from IPFS with CID: {cid}")

    def close(self):
        """Close the IPFS client connection."""
        self.client.close()
        logging.info("IPFS client closed.")

# Example usage
if __name__ == "__main__":
    ipfs = IPFSStorage()
    cid = ipfs.add_file("example.txt")  # Ensure you have a file named example.txt in the same directory
    ipfs.get_file(cid, "retrieved_example.txt")
    ipfs.close()
