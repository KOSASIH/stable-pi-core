# src/generative_ai/data_collection.py

import requests

class DataCollector:
    def __init__(self, api_url):
        self.api_url = api_url

    def collect_data(self):
        """Collect data from the specified API."""
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to collect data: {response.status_code}")
