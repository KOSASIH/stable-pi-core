import paho.mqtt.client as mqtt
import logging
import json
import os
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt.example.com")  # Replace with your MQTT broker
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))                # Default MQTT port
DEVICE_ID = os.getenv("DEVICE_ID", "device123")              # Unique ID for the IoT device

# Callback when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected to MQTT Broker: {MQTT_BROKER} with result code {rc}")
    # Subscribe to a topic for receiving commands
    client.subscribe(f"iot/devices/{DEVICE_ID}/commands")

# Callback when a message is received from the server
def on_message(client, userdata, msg):
    logging.info(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    # Here you can add logic to handle the received message
    # For example, you could execute a command based on the message content

# Initialize MQTT client
mqtt_client = mqtt.Client()

# Assign the callback functions
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def start_mqtt_client():
    """Start the MQTT client for the IoT device."""
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()  # Start the loop to process network traffic
        logging.info("MQTT client started.")
    except Exception as e:
        logging.error(f"Failed to connect to MQTT Broker: {e}")

def publish_data(data):
    """Publish data to the MQTT broker."""
    try:
        mqtt_client.publish(f"iot/devices/{DEVICE_ID}/data", json.dumps(data))
        logging.info(f"Published data: {data} to topic: iot/devices/{DEVICE_ID}/data")
    except Exception as e:
        logging.error(f"Error publishing data: {e}")

if __name__ == '__main__':
    start_mqtt_client()
    try:
        while True:
            # Simulate sending data from the IoT device
            simulated_data = {
                "temperature": 22.5,
                "humidity": 60,
                "device_id": DEVICE_ID
            }
            publish_data(simulated_data)
            time.sleep(5)  # Send data every 5 seconds
    except KeyboardInterrupt:
        logging.info("Disconnecting from MQTT Broker...")
        mqtt_client.loop_stop()  # Stop the loop
        mqtt_client.disconnect()  # Disconnect from the broker
        logging.info("Disconnected from MQTT Broker.")
