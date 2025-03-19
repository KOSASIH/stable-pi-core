# nodes/node_network.py

from flask import Flask, request, jsonify
from .node import Node
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

class NodeNetwork:
    def __init__(self, encryption_key):
        self.nodes = {}
        self.encryption_key = encryption_key
        self.app = Flask(__name__)

        @self.app.route('/register_node', methods=['POST'])
        def register_node():
            """Endpoint to register a new node."""
            data = request.json
            node_id = data['node_id']
            api_url = data['api_url']
            if node_id not in self.nodes:
                self.nodes[node_id] = Node(node_id, api_url, self.encryption_key)
                logging.info(f"Node {node_id} registered successfully.")
                return jsonify({"message": "Node registered successfully."}), 201
            return jsonify({"message": "Node already exists."}), 400

        @self.app.route('/receive_data', methods=['POST'])
        def receive_data():
            """Endpoint to receive data from a node."""
            data = request.json
            node_id = data['node_id']
            if node_id in self.nodes:
                asyncio.run(self.nodes[node_id].receive_data(data))
                return jsonify({"message": "Data received successfully."}), 200
            return jsonify({"message": "Node not found."}), 404

    def start(self, host='0.0.0.0', port=5000):
        """Starts the Flask application."""
        self.app.run(host=host, port=port)

    def create_node(self, node_id, api_url):
        """Creates a new node and adds it to the network."""
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, api_url, self.encryption_key)
            logging.info(f"Node {node_id} created and added to the network.")
        else:
            logging.warning(f"Node {node_id} already exists in the network.")

    def discover_nodes(self):
        """Dynamically discovers nodes in the network."""
        # This method can be implemented to periodically check for new nodes
        logging.info("Discovering nodes in the network...")
