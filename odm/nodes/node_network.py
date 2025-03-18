"""
Node Network Module

This module manages the network of nodes, including communication and
data sharing among nodes.
"""

from flask import Flask, request, jsonify

class NodeNetwork:
    def __init__(self):
        self.app = Flask(__name__)
        self.nodes = {}  # Dictionary to hold nodes by their ID
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/register_node', methods=['POST'])
        def register_node():
            data = request.json
            node_id = data.get('node_id')
            location = data.get('location')
            if node_id and location:
                self.nodes[node_id] = location
                return jsonify({"message": f"Node {node_id} registered successfully!"}), 201
            return jsonify({"error": "Node ID and location are required."}), 400

        @self.app.route('/data', methods=['POST'])
        def receive_data():
            data = request.json
            # Process the received data (e.g., store it, analyze it)
            print("Data received from nodes:", data)
            return jsonify({"message": "Data received successfully!"}), 200

    def run(self, host='0.0.0.0', port=5000):
        """
        Run the Flask application for the node network.

        :param host: Host address to run the server on
        :param port: Port to run the server on
        """
        self.app.run(host=host, port=port)
