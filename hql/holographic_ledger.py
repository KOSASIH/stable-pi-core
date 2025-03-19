# hql/holographic_ledger.py

import json
import logging
from .quantum_interference import QuantumInterference
from .config import Config
from datetime import datetime, timedelta

class HolographicQuantumLedger:
    def __init__(self):
        self.data_store = {}
        self.quantum_interference = QuantumInterference()
        self.load_data()
        logging.info("Holographic Quantum Ledger initialized.")

    def store_data(self, key, value):
        """
        Store data in the holographic ledger.
        :param key: The key for the data.
        :param value: The value to store.
        """
        if len(self.data_store) >= Config.DEFAULTS["MAX_DATA_ENTRIES"]:
            self.cleanup_old_entries()
        
        holographic_data = self.quantum_interference.encode(value)
        self.data_store[key] = {
            "data": holographic_data,
            "timestamp": datetime.now()
        }
        logging.info(f"Data stored under key '{key}'.")

    def retrieve_data(self, key):
        """
        Retrieve data from the holographic ledger.
        :param key: The key for the data.
        :return: The retrieved value or None if not found.
        """
        entry = self.data_store.get(key)
        if entry:
            value = self.quantum_interference.decode(entry["data"])
            logging.info(f"Data retrieved for key '{key}'.")
            return value
        else:
            logging.warning(f"No data found for key '{key}'.")
            return None

    def export_data(self, filename=None):
        """
        Export the entire data store to a JSON file.
        :param filename: The name of the file to export to. Defaults to the configured ledger filename.
        """
        if filename is None:
            filename = Config.DEFAULTS["LEDGER_FILENAME"]
        
        with open(filename, 'w') as f:
            json.dump(self.data_store, f, default=str)
        logging.info(f"Data exported to {filename}.")

    def import_data(self, filename=None):
        """
        Import data from a JSON file into the ledger.
        :param filename: The name of the file to import from. Defaults to the configured ledger filename.
        """
        if filename is None:
            filename = Config.DEFAULTS["LEDGER_FILENAME"]
        
        with open(filename, 'r') as f:
            self.data_store = json.load(f)
            # Decode the holographic data
            for key, entry in self.data_store.items():
                entry["data"] = self.quantum_interference.decode(entry["data"])
        logging.info(f"Data imported from {filename}.")

    def cleanup_old_entries(self):
        """
        Remove old entries from the data store based on the retention period.
        """
        retention_period = timedelta(days=Config.DEFAULTS["DATA_RETENTION_PERIOD"])
        cutoff_time = datetime.now() - retention_period
        keys_to_delete = [key for key, entry in self.data_store.items() if entry["timestamp"] < cutoff_time]

        for key in keys_to_delete:
            del self.data_store[key]
            logging.info(f"Removed old entry for key '{key}'.")

    def load_data(self):
        """
        Load existing data from the configured ledger file.
        """
        if os.path.exists(Config.DEFAULTS["LEDGER_FILENAME"]):
            self.import_data(Config.DEFAULTS["LEDGER_FILENAME"])
        else:
            logging.info("No existing ledger file found. Starting with an empty ledger.")
