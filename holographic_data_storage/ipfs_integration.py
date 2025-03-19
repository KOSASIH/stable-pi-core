import ipfshttpclient
import logging

class IPFSIntegration:
    """
    A class to manage the integration with IPFS for data distribution.

    Attributes:
        client (ipfshttpclient.Client): The IPFS client instance.
    """

    def __init__(self, ipfs_address: str = '/dns/localhost/tcp/5001/http'):
        """
        Initializes the IPFSIntegration instance.

        Args:
            ipfs_address (str): The address of the IPFS node to connect to.
        """
        self.client = ipfshttpclient.connect(ipfs_address)
        logging.basicConfig(level=logging.INFO)

    def upload_data(self, data: bytes) -> str:
        """
        Uploads data to IPFS and returns the content identifier (CID).

        Args:
            data (bytes): The data to upload.

        Returns:
            str: The content identifier (CID) of the uploaded data.
        """
        try:
            result = self.client.add_bytes(data)
            cid = result['cid']
            logging.info(f"Data uploaded to IPFS with CID: {cid}")
            return cid
        except Exception as e:
            logging.error(f"Failed to upload data to IPFS: {e}")
            return None

    def retrieve_data(self, cid: str) -> bytes:
        """
        Retrieves data from IPFS using the content identifier (CID).

        Args:
            cid (str): The content identifier (CID) of the data to retrieve.

        Returns:
            bytes: The retrieved data.
        """
        try:
            data = self.client.cat(cid)
            logging.info(f"Data retrieved from IPFS with CID: {cid}")
            return data
        except Exception as e:
            logging.error(f"Failed to retrieve data from IPFS: {e}")
            return None

    def pin_data(self, cid: str) -> bool:
        """
        Pins data to the IPFS node to ensure it remains available.

        Args:
            cid (str): The content identifier (CID) of the data to pin.

        Returns:
            bool: True if the data was pinned successfully, False otherwise.
        """
        try:
            self.client.pin.add(cid)
            logging.info(f"Data pinned to IPFS with CID: {cid}")
            return True
        except Exception as e:
            logging.error(f"Failed to pin data to IPFS: {e}")
            return False

    def unpin_data(self, cid: str) -> bool:
        """
        Unpins data from the IPFS node.

        Args:
            cid (str): The content identifier (CID) of the data to unpin.

        Returns:
            bool: True if the data was unpinned successfully, False otherwise.
        """
        try:
            self.client.pin.rm(cid)
            logging.info(f"Data unpinned from IPFS with CID: {cid}")
            return True
        except Exception as e:
            logging.error(f"Failed to unpin data from IPFS: {e}")
            return False
