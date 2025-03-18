"""
Node Module

This module implements the individual node for data collection in the
space-based node network.
"""

import random
import time
import json
import requests

class Node:
    def __init__(self, node_id, location):
        self.node_id = node_id
        self.location = location
        self.data = []  # List to hold collected data

    def collect_data(self):
        """
        Simulate data collection from sensors or external sources.
        """
        # Simulate data collection with random values
        collected_data = {
            "node_id": self.node_id,
            "location": self.location,
            "temperature": random.uniform(-50, 50),  # Simulated temperature data
            "humidity": random.uniform(0, 100),      # Simulated humidity data
            "timestamp": time.time()
        }
        self.data.append(collected_data)
        print(f"Data collected by Node {self.node_id}: {collected_data}")

    def send_data(self, network_url):
        """
        Send collected data to the specified network URL.

        :param network_url: URL of the node network to send data to
        """
        if self.data:
            response = requests.post(network_url, json=self.data)
            if response.status_code == 200:
                print(f"Data sent successfully from Node {self.node_id}.")
                self.data.clear()  # Clear data after successful send
            else:
                print(f"Failed to send data from Node {self.node_id}: {response.text}")
        else:
            print(f"No data to send from Node {self.node_id}.")
