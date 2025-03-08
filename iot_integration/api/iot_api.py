from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
import logging
import json
from web3 import Web3
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt.example.com")  # Replace with your MQTT broker
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

# Initialize MQTT client
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    logging.info("Connected to MQTT Broker")

mqtt_client.on_connect = on_connect
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()  # Start the MQTT client loop

# Ethereum Configuration
ETHEREUM_NODE = os.getenv("ETHEREUM_NODE", "https://your.ethereum.node")  # Replace with your Ethereum node URL
w3 = Web3(Web3.HTTPProvider(ETHEREUM_NODE))

# Replace with your contract address and ABI
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "0xYourContractAddress")
CONTRACT_ABI = json.loads(os.getenv("CONTRACT_ABI", '[{"constant":true,"inputs":[],"name":"yourFunction","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'))

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

@app.route('/iot/data', methods=['POST'])
def receive_data():
    """Receive data from IoT devices and publish to MQTT."""
    try:
        data = request.json
        logging.info(f"Received data: {data}")

        # Validate incoming data
        if 'device_id' not in data or 'temperature' not in data or 'humidity' not in data:
            logging.error("Invalid data format.")
            return jsonify({"status": "error", "message": "Invalid data format."}), 400

        # Publish data to MQTT
        mqtt_client.publish(f"iot/devices/{data['device_id']}/data", json.dumps(data))
        
        return jsonify({"status": "success", "message": "Data received and published."}), 200
    except Exception as e:
        logging.error(f"Error receiving data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/iot/transaction', methods=['POST'])
def create_transaction():
    """Create a transaction on the blockchain based on IoT data."""
    try:
        transaction_data = request.json
        logging.info(f"Creating transaction: {transaction_data}")

        # Validate incoming transaction data
        if 'from_address' not in transaction_data or 'amount' not in transaction_data:
            logging.error("Invalid transaction data format.")
            return jsonify({"status": "error", "message": "Invalid transaction data format."}), 400

        # Example: Sending a transaction to the Ethereum blockchain
        tx = {
            'to': CONTRACT_ADDRESS,
            'value': w3.toWei(transaction_data['amount'], 'ether'),  # Amount in Ether
            'gas': 2000000,
            'gasPrice': w3.toWei('50', 'gwei'),
            'nonce': w3.eth.getTransactionCount(transaction_data['from_address']),
        }

        # Sign the transaction (replace with your private key)
        signed_tx = w3.eth.account.signTransaction(tx, private_key=os.getenv("PRIVATE_KEY", "0xYourPrivateKey"))
        
        # Send the transaction
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        logging.info(f"Transaction sent: {tx_hash.hex()}")

        return jsonify({"status": "success", "message": "Transaction created.", "tx_hash": tx_hash.hex()}), 200
    except Exception as e:
        logging.error(f"Error creating transaction: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the Flask app
