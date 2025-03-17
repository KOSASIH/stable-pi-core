# stsp/cross_chain/cross_chain_utils.py

import logging
import json

def generate_cross_chain_message(data):
    """
    Generate a cross-chain message for transferring data.

    :param data: The data to include in the message.
    :return: A formatted cross-chain message.
    """
    message = {
        "type": "cross_chain_transfer",
        "data": data,
        "timestamp": time.time()
    }
    logging.info("Generated cross-chain message: %s", message)
    return message

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Simulate generating a cross-chain message
    data = {"sensor_data": [1, 2, 3, 4, 5]}
    message = generate_cross_chain_message(data)
    print(f"Generated Cross-Chain Message: {message}")
