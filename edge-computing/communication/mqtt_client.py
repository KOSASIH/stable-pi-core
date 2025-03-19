import paho.mqtt.client as mqtt
import yaml
import json
import logging
import time
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open('config/mqtt-config.yaml', 'r') as file:
    mqtt_config = yaml.safe_load(file)

# MQTT settings
broker_host = mqtt_config['mqtt']['broker']['host']
broker_port = mqtt_config['mqtt']['broker']['port']
client_id = mqtt_config['mqtt']['broker']['client_id']
data_topic = mqtt_config['mqtt']['topics']['data_collection']
control_topic = mqtt_config['mqtt']['topics']['control_commands']
qos = mqtt_config['mqtt'].get('qos', 1)  # Default QoS level

# Callback function for when a message is received
def on_message(client, userdata, msg):
    logging.info(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

# Callback function for connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT broker.")
        client.subscribe(control_topic)
    else:
        logging.error(f"Failed to connect to MQTT broker, return code: {rc}")

# Callback function for disconnection
def on_disconnect(client, userdata, rc):
    logging.info("Disconnected from MQTT broker.")
    if rc != 0:
        logging.warning("Unexpected disconnection. Attempting to reconnect...")
        reconnect(client)

# Reconnect logic
def reconnect(client):
    while True:
        try:
            client.reconnect()
            logging.info("Reconnected to MQTT broker.")
            break
        except Exception as e:
            logging.error(f"Reconnect failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# Create an MQTT client
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Connect to the MQTT broker
try:
    client.connect(broker_host, broker_port, keepalive=60)
except Exception as e:
    logging.error(f"Failed to connect to MQTT broker: {e}")
    exit(1)

# Start the loop
client.loop_start()

try:
    while True:
        # Simulate publishing sensor data
        sensor_data = {
            'temperature': round(random.uniform(20.0, 30.0), 2),
            'humidity': round(random.uniform(30.0, 70.0), 2),
            'timestamp': time.time()
        }
        client.publish(data_topic, json.dumps(sensor_data), qos=qos)
        logging.info(f"Published data: {sensor_data} to topic: {data_topic}")
        
        # Wait before publishing the next message
        time.sleep(5)

except KeyboardInterrupt:
    logging.info("MQTT client stopped by user.")

finally:
    client.loop_stop()
    client.disconnect()
    logging.info("Disconnected from MQTT broker.")
