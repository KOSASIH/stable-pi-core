import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Bridge:
    def __init__(self, source_chain: str, target_chain: str, api_url: str):
        """Initialize the bridge between two blockchains."""
        self.source_chain = source_chain
        self.target_chain = target_chain
        self.api_url = api_url
        logging.info(f"Bridge initialized between {source_chain} and {target_chain}")

    def transfer_asset(self, asset_id: str, amount: float, recipient: str) -> dict:
        """Transfer an asset from the source chain to the target chain."""
        logging.info(f"Initiating transfer of {amount} of asset {asset_id} to {recipient} on {self.target_chain}")
        payload = {
            "asset_id": asset_id,
            "amount": amount,
            "recipient": recipient
        }
        response = requests.post(f"{self.api_url}/transfer", json=payload)

        if response.status_code == 200:
            logging.info("Transfer successful.")
            return response.json()
        else:
            logging.error(f"Transfer failed with status code: {response.status_code}")
            return {"error": "Transfer failed", "status_code": response.status_code}

# Example usage
if __name__ == "__main__":
    bridge = Bridge(source_chain="Ethereum", target_chain="Binance Smart Chain", api_url="https://api.example.com/bridge")
    
    # Simulate asset transfer
    result = bridge.transfer_asset(asset_id="ETH", amount=1.0, recipient="0xRecipientAddress")
    print(f"Transfer Result: {result}")
