import time
import random
import json

class QuantumWormholeGateway:
    def __init__(self):
        self.nodes = {}
        self.transaction_log = []

    def register_node(self, node_id, location, auth_token):
        """Register a new node with an authentication token."""
        if self.authenticate(auth_token):
            self.nodes[node_id] = {'location': location, 'status': 'active'}
            print(f"Node {node_id} registered at {location}.")
        else:
            raise PermissionError("Invalid authentication token.")

    def authenticate(self, auth_token):
        """Simulate authentication (in a real scenario, this would check against a secure database)."""
        # For demonstration, let's assume any token that starts with 'secure-' is valid
        return auth_token.startswith('secure-')

    def transfer_asset(self, asset, amount, from_node, to_node):
        """Transfer assets between registered nodes."""
        if from_node not in self.nodes or to_node not in self.nodes:
            raise ValueError("Both nodes must be registered.")
        
        if self.nodes[from_node]['status'] != 'active' or self.nodes[to_node]['status'] != 'active':
            raise ValueError("One or both nodes are inactive.")

        # Simulate transfer delay
        print(f"Initiating transfer of {amount} {asset} from {from_node} to {to_node} via Quantum Wormhole...")
        time.sleep(random.uniform(0.5, 2.0))  # Simulate network delay
        self.log_transaction(asset, amount, from_node, to_node)
        print(f"Transfer complete: {amount} {asset} has been sent to {to_node}.")

    def log_transaction(self, asset, amount, from_node, to_node):
        """Log the transaction details."""
        transaction = {
            'asset': asset,
            'amount': amount,
            'from_node': from_node,
            'to_node': to_node,
            'timestamp': time.time()
        }
        self.transaction_log.append(transaction)
        print(f"Transaction logged: {json.dumps(transaction)}")

    def get_transaction_log(self):
        """Retrieve the transaction log."""
        return self.transaction_log

    def check_node_status(self, node_id):
        """Check the status of a node."""
        if node_id in self.nodes:
            return self.nodes[node_id]['status']
        else:
            raise ValueError("Node not found.")

    def deactivate_node(self, node_id):
        """Deactivate a node."""
        if node_id in self.nodes:
            self.nodes[node_id]['status'] = 'inactive'
            print(f"Node {node_id} has been deactivated.")
        else:
            raise ValueError("Node not found.")

    def activate_node(self, node_id):
        """Activate a node."""
        if node_id in self.nodes:
            self.nodes[node_id]['status'] = 'active'
            print(f"Node {node_id} has been activated.")
        else:
            raise ValueError("Node not found.")

# Example usage
if __name__ == "__main__":
    qwg = QuantumWormholeGateway()
    qwg.register_node("Node_Mars", "Mars", "secure-token-123")
    qwg.register_node("Node_Proxima", "Proxima Centauri", "secure-token-456")
    
    try:
        qwg.transfer_asset("CNC", 100, "Node_Mars", "Node_Proxima")
        print("Transaction Log:", qwg.get_transaction_log())
    except Exception as e:
        print(f"Error: {e}")

    # Check node status
    print("Node Mars Status:", qwg.check_node_status("Node_Mars"))
    
    # Deactivate and reactivate a node
    qwg.deactivate_node("Node_Mars")
    print("Node Mars Status after deactivation:", qwg.check_node_status("Node_Mars"))
    qwg.activate_node("Node_Mars")
    print("Node Mars Status after reactivation:", qwg.check_node_status("Node_Mars"))
