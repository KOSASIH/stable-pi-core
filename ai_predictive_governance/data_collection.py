import requests
import json
from typing import List, Dict, Any

class DataCollector:
    """
    A class to collect on-chain and off-chain data for AI-driven predictive governance.

    Attributes:
        on_chain_url (str): The URL of the blockchain API to collect on-chain data.
        off_chain_sources (List[str]): A list of URLs for off-chain data sources.
    """

    def __init__(self, on_chain_url: str, off_chain_sources: List[str]):
        self.on_chain_url = on_chain_url
        self.off_chain_sources = off_chain_sources

    def collect_on_chain_data(self) -> Dict[str, Any]:
        """
        Collects on-chain data from the specified blockchain API.

        Returns:
            Dict[str, Any]: The on-chain data collected from the blockchain API.
        """
        try:
            response = requests.get(self.on_chain_url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error collecting on-chain data: {e}")
            return {}

    def collect_off_chain_data(self) -> List[Dict[str, Any]]:
        """
        Collects off-chain data from the specified sources.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the off-chain data.
        """
        data = []
        for source in self.off_chain_sources:
            try:
                response = requests.get(source)
                response.raise_for_status()  # Raise an error for bad responses
                data.append(response.json())
            except requests.exceptions.RequestException as e:
                print(f"Error collecting off-chain data from {source}: {e}")
        return data

    def collect_data(self) -> Dict[str, Any]:
        """
        Collects both on-chain and off-chain data.

        Returns:
            Dict[str, Any]: A dictionary containing both on-chain and off-chain data.
        """
        on_chain_data = self.collect_on_chain_data()
        off_chain_data = self.collect_off_chain_data()
        return {
            "on_chain": on_chain_data,
            "off_chain": off_chain_data
        }
