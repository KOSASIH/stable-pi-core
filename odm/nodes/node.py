# nodes/node.py

import json
import random
import aiohttp
import asyncio
from cryptography.fernet import Fernet
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

class Node:
    def __init__(self, node_id, api_url, encryption_key):
        self.node_id = node_id
        self.api_url = api_url
        self.data = []
        self.cipher = Fernet(encryption_key)

    def collect_data(self, new_data):
        """Collects new data and adds it to the node's data list."""
        self.data.append(new_data)
        logging.info(f"Node {self.node_id} collected data: {new_data}")

    async def send_data(self, target_node):
        """Sends collected data to another node asynchronously."""
        if self.data:
            encrypted_data = self.cipher.encrypt(json.dumps(self.data).encode())
            payload = {
                'node_id': self.node_id,
                'data': encrypted_data.decode()
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{target_node.api_url}/receive_data", json=payload) as response:
                    if response.status == 200:
                        logging.info(f"Node {self.node_id} sent data to Node {target_node.node_id}")
                        self.data.clear()  # Clear data after sending
                    else:
                        logging.error(f"Failed to send data from Node {self.node_id} to Node {target_node.node_id}")

    async def receive_data(self, data):
        """Receives data from another node asynchronously."""
        decrypted_data = self.cipher.decrypt(data['data'].encode())
        self.data.extend(json.loads(decrypted_data))
        logging.info(f"Node {self.node_id} received data: {data['data']}")
