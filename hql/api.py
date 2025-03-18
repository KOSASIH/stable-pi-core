# hql/api.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from .holographic_ledger import HolographicQuantumLedger
from .config import Config
import logging

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing
ledger = HolographicQuantumLedger()

# Set up logging
logging.basicConfig(level=Config.DEFAULTS["LOGGING_LEVEL"],
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/store', methods=['POST'])
def store_data():
    """Store data in the holographic ledger."""
    data = request.json
    key = data.get('key')
    value = data.get('value')

    if not key or not value:
        logging.error("Key and value must be provided.")
        return jsonify({"error": "Key and value must be provided."}), 400

    try:
        ledger.store_data(key, value)
        return jsonify({"message": "Data stored successfully."}), 201
    except Exception as e:
        logging.error(f"Error storing data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/retrieve/<string:key>', methods=['GET'])
def retrieve_data(key):
    """Retrieve data from the holographic ledger."""
    try:
        value = ledger.retrieve_data(key)
        if value is not None:
            return jsonify({"key": key, "value": value}), 200
        else:
            return jsonify({"error": "Data not found."}), 404
    except Exception as e:
        logging.error(f"Error retrieving data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/export', methods=['GET'])
def export_data():
    """Export the entire data store to a JSON file."""
    try:
        ledger.export_data()
        return jsonify({"message": "Data exported successfully."}), 200
    except Exception as e:
        logging.error(f"Error exporting data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/import', methods=['POST'])
def import_data():
    """Import data from a JSON file into the ledger."""
    filename = request.json.get('filename', Config.DEFAULTS["LEDGER_FILENAME"])
    
    try:
        ledger.import_data(filename)
        return jsonify({"message": "Data imported successfully."}), 200
    except Exception as e:
        logging.error(f"Error importing data: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
