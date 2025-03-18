# dmec/data_handler.py

import json
import os

class DataHandler:
    def __init__(self, filename='energy_data.json'):
        self.filename = filename
        self.data = []

    def save_data(self, energy_output):
        self.data.append(energy_output)
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        return self.data
