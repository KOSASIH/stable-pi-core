# nbca/api.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from .neutrino_detector import NeutrinoDetector
from .data_processing import DataProcessing
from .communication_protocol import CommunicationProtocol
import logging

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Initialize components
detector = NeutrinoDetector(detector_type="IceCube")
data_processor = DataProcessing()
communication_protocol = CommunicationProtocol(data_format="JSON")

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/detect_event', methods=['POST'])
def detect_event():
    """Detect a neutrino event."""
    event = detector.detect_event()
    if event:
        logging.info(f"Detected event: {event}")
        return jsonify(event), 200
    else:
        return jsonify({"error": "No event detected."}), 404

@app.route('/process_event', methods=['POST'])
def process_event():
    """Process a detected neutrino event."""
    event = request.json
    if not event:
        return jsonify({"error": "Event data must be provided."}), 400

    processed_data = data_processor.process_event(event)
    return jsonify(processed_data), 200

@app.route('/send_data', methods=['POST'])
def send_data():
    """Send processed data to a specified destination."""
    data = request.json
    destination = data.get("destination")
    if not destination or "data" not in data:
        return jsonify({"error": "Destination and data must be provided."}), 400

    response = communication_protocol.send_data(data["data"], destination)
    return jsonify(response), 200

@app.route('/receive_data', methods=['POST'])
def receive_data():
    """Receive encoded data from a source."""
    encoded_data = request.json.get("encoded_data")
    if not encoded_data:
        return jsonify({"error": "Encoded data must be provided."}), 400

    data = communication_protocol.receive_data(encoded_data)
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
