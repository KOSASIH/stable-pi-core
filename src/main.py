import os
import asyncio
from flask import Flask, jsonify, request
from flask_cors import CORS
from storage.blockchain import Blockchain
from consensus.consensus_manager import ConsensusManager
from network.api import create_api
from utils.logger import setup_logger
from utils.exceptions import CustomException

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Set up logging
logger = setup_logger()

# Initialize the blockchain and consensus manager
blockchain = Blockchain()
consensus_manager = ConsensusManager(blockchain)

# Create the API and register the routes
api = create_api(blockchain, consensus_manager)
app.register_blueprint(api)

@app.route('/')
def home() -> jsonify:
    """Home route to check the status of the API."""
    latest_block = blockchain.chain[-1].to_dict() if blockchain.chain else None
    return jsonify({
        "message": "Welcome to the Ultra-Advanced Stable-Pi-Core Blockchain API",
        "status": "Running",
        "block_count": len(blockchain.chain),
        "latest_block": latest_block
    })

@app.route('/mine', methods=['POST'])
async def mine_block() -> jsonify:
    """Route to mine a new block."""
    try:
        data = request.get_json()
        if not data or 'data' not in data:
            raise CustomException("Invalid data", 400)

        # Asynchronously mine a new block
        new_block = await asyncio.to_thread(blockchain.add_block, data['data'])
        await asyncio.to_thread(consensus_manager.handle_new_block, new_block)

        logger.info(f"New block mined: {new_block.index}")
        return jsonify(new_block.to_dict()), 201

    except CustomException as e:
        logger.error(f"Error: {e.message}")
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/chain', methods=['GET'])
def get_chain() -> jsonify:
    """Route to retrieve the entire blockchain."""
    return jsonify(blockchain.to_dict()), 200

@app.route('/validate', methods=['POST'])
async def validate_chain() -> jsonify:
    """Route to validate the blockchain."""
    try:
        is_valid = await asyncio.to_thread(blockchain.validate_chain)
        return jsonify({"is_valid": is_valid}), 200
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({"error": "Chain validation failed."}), 500

@app.route('/stats', methods=['GET'])
async def get_stats() -> jsonify:
    """Route to retrieve blockchain statistics."""
    try:
        latest_block = blockchain.chain[-1].to_dict() if blockchain.chain else None
        stats = {
            "block_count": len(blockchain.chain),
            "latest_block": latest_block,
            "consensus_status": consensus_manager.get_status()
        }
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Error retrieving stats: {str(e)}")
        return jsonify({"error": "Failed to retrieve statistics."}), 500

if __name__ == '__main__':
    # Load environment variables
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")

    # Start the Flask application
    logger.info(f"Starting the application on {host}:{port}")
    app.run(host=host, port=port, threaded=True)
