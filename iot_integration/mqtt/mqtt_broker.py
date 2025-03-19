import paho.mqtt.client as mqtt
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt.example.com")  # Replace with your MQTT broker
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))                # Default MQTT port

# Callback when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected to MQTT Broker: {MQTT_BROKER} with result code {rc}")
    # Subscribe to a topic (e.g., for receiving data from IoT devices)
    client.subscribe("iot/devices/#")  # Subscribe to all device topics

# Callback when a message is received from the server
def on_message(client, userdata, msg):
    logging.info(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    # Here you can add logic to handle the received message

# Initialize MQTT client
mqtt_client = mqtt.Client()

# Assign the callback functions
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def start_mqtt_broker():
    """Start the MQTT broker client."""
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()  # Start the loop to process network traffic
        logging.info("MQTT broker client started.")
    except Exception as e:
        logging.error(f"Failed to connect to MQTT Broker: {e}")

if __name__ == '__main__':
    start_mqtt_broker()
    try:
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        logging.info("Disconnecting from MQTT Broker...")
        mqtt_client.loop_stop()  # Stop the loop
        mqtt_client.disconnect()  # Disconnect from the broker
        logging.info("Disconnected from MQTT Broker.")
