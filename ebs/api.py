# ebs/api.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from .signal_detector import SignalDetector
from .blockchain_sync import BlockchainSync
from .ai_security import AISecurity
import logging

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Initialize components
signal_detector = SignalDetector()
blockchain_sync = BlockchainSync(blockchain_url="http://example-blockchain.com/api")  # Replace with actual URL
ai_security = AISecurity()

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/detect_signal', methods=['POST'])
def detect_signal():
    """Detect a signal from space."""
    duration = request.json.get('duration', 10)  # Default to 10 seconds
    detected_signals = signal_detector.listen_for_signals(duration=duration)
    return jsonify({"detected_signals": detected_signals}), 200

@app.route('/sync', methods=['POST'])
def sync_with_blockchain():
    """Synchronize data with the external blockchain network."""
    data = request.json
    response = blockchain_sync.sync_with_external_network(data)
    if response:
        return jsonify(response), 200
    else:
        return jsonify({"error": "Synchronization failed."}), 500

@app.route('/analyze_signal', methods=['POST'])
def analyze_signal():
    """Analyze a detected signal for security purposes."""
    signal = request.json.get('signal')
    if not signal:
        return jsonify({"error": "Signal must be provided."}), 400

    result = ai_security.analyze_signal(signal)
    return jsonify({"analysis_result": result}), 200

@app.route('/assess_threat', methods=['POST'])
def assess_threat():
    """Assess the threat level of the data being synchronized."""
    data = request.json.get('data')
    if not data:
        return jsonify({"error": "Data must be provided."}), 400

    result = ai_security.assess_threat(data)
    return jsonify({"threat_assessment_result": result}), 200

@app.route('/set_sync_attempts', methods=['POST'])
def set_sync_attempts():
    """Set the maximum number of sync attempts."""
    attempts = request.json.get('attempts')
    if attempts is None or attempts <= 0:
        return jsonify({"error": "Attempts must be a positive integer."}), 400

    blockchain_sync.set_max_sync_attempts(attempts)
    return jsonify({"message": f"Max sync attempts set to {attempts}."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
