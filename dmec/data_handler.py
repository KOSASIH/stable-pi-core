# dmec/data_handler.py

import json
import os
import csv
import logging
from datetime import datetime
from .config import Config

class DataHandler:
    def __init__(self):
        self.json_filename = Config.DEFAULTS["DATA_FILENAME"]
        self.csv_filename = Config.DEFAULTS["CSV_FILENAME"]
        self.data = []

        # Load existing data
        self.load_data()

    def save_data(self, energy_output):
        """
        Save the energy output data to the specified format (JSON or CSV).
        :param energy_output: The energy output to save.
        """
        timestamp = datetime.now().isoformat()
        self.data.append((timestamp, energy_output))
        self.save_to_json(timestamp, energy_output)
        self.save_to_csv(timestamp, energy_output)

    def save_to_json(self, timestamp, energy_output):
        """
        Save the energy output to a JSON file.
        :param timestamp: The timestamp of the energy output.
        :param energy_output: The energy output to save.
        """
        try:
            with open(self.json_filename, 'w') as f:
                json.dump(self.data, f)
            logging.info(f"Data saved to JSON: {timestamp}, {energy_output} units")
        except Exception as e:
            logging.error(f"Error saving to JSON: {e}")

    def save_to_csv(self, timestamp, energy_output):
        """
        Save the energy output to a CSV file.
        :param timestamp: The timestamp of the energy output.
        :param energy_output: The energy output to save.
        """
        try:
            with open(self.csv_filename, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, energy_output])
            logging.info(f"Data saved to CSV: {timestamp}, {energy_output} units")
        except Exception as e:
            logging.error(f"Error saving to CSV: {e}")

    def load_data(self):
        """
        Load existing data from JSON and CSV files.
        """
        if os.path.exists(self.json_filename):
            try:
                with open(self.json_filename, 'r') as f:
                    self.data = json.load(f)
                logging.info(f"Data loaded from JSON: {len(self.data)} records found.")
            except Exception as e:
                logging.error(f"Error loading JSON data: {e}")

        if os.path.exists(self.csv_filename):
            try:
                with open(self.csv_filename, 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        self.data.append((row[0], float(row[1])))
                logging.info(f"Data loaded from CSV: {len(self.data)} records found.")
            except Exception as e:
                logging.error(f"Error loading CSV data: {e}")

    def get_data(self):
        """
        Return the loaded data.
        :return: List of tuples containing timestamp and energy output.
        """
        return self.data
